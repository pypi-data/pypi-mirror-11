/*
Copyright (c) by respective owners including Yahoo!, Microsoft, and
individual contributors. All rights reserved.  Released under a BSD (revised)
license as described in the file LICENSE.
 */
#include <float.h>
#include <errno.h>

#include "reductions.h"
#include "v_hashmap.h"
#include "label_dictionary.h"
#include "vw.h"
#include "gd.h" // GD::foreach_feature() needed in subtract_example()
#include "vw_exception.h"

using namespace std;
using namespace LEARNER;
using namespace COST_SENSITIVE;

struct csoaa{
  uint32_t num_classes;
  polyprediction* pred;
};

template<bool is_learn>
inline void inner_loop(base_learner& base, example& ec, uint32_t i, float cost,
                       uint32_t& prediction, float& score, float& partial_prediction) {
  if (is_learn) {
    ec.l.simple.label = cost;
    ec.l.simple.weight = (cost == FLT_MAX) ? 0.f : 1.f;
    base.learn(ec, i-1);
  } else
    base.predict(ec, i-1);

  partial_prediction = ec.partial_prediction;
  if (ec.partial_prediction < score || (ec.partial_prediction == score && i < prediction)) {
    score = ec.partial_prediction;
    prediction = i;
  }
}

#define DO_MULTIPREDICT true

template <bool is_learn>
void predict_or_learn(csoaa& c, base_learner& base, example& ec) {
  COST_SENSITIVE::label ld = ec.l.cs;
  /*
  if (ld.costs.size() == 1) {
    ec.pred.multiclass = ld.costs[0].class_index;
    return;
  }
  */
  uint32_t prediction = 1;
  float score = FLT_MAX;
  ec.l.simple = { 0., 0., 0. };
  if (ld.costs.size() > 0) {
    for (wclass *cl = ld.costs.begin; cl != ld.costs.end; cl ++)
      inner_loop<is_learn>(base, ec, cl->class_index, cl->x, prediction, score, cl->partial_prediction);
    ec.partial_prediction = score;
  } else if (DO_MULTIPREDICT && !is_learn) {
    ec.l.simple = { FLT_MAX, 0.f, 0.f };
    base.multipredict(ec, 0, c.num_classes, c.pred, false);
    for (uint32_t i = 1; i <= c.num_classes; i++)
      if (c.pred[i-1].scalar < c.pred[prediction-1].scalar)
        prediction = i;
    ec.partial_prediction = c.pred[prediction-1].scalar;
    //cerr << "c.num_classes = " << c.num_classes << ", prediction = " << prediction << endl;
  } else {
    float temp;
    for (uint32_t i = 1; i <= c.num_classes; i++)
      inner_loop<false>(base, ec, i, FLT_MAX, prediction, score, temp);
    ec.partial_prediction = score;
  }

  ec.pred.multiclass = prediction;
  ec.l.cs = ld;
}

void finish_example(vw& all, csoaa&, example& ec)
{
  output_example(all, ec);
  VW::finish_example(all, &ec);
}

void finish(csoaa& c) {
  free(c.pred);
}


base_learner* csoaa_setup(vw& all)
{
  if (missing_option<size_t, true>(all, "csoaa", "One-against-all multiclass with <k> costs"))
    return nullptr;

  csoaa& c = calloc_or_die<csoaa>();
  c.num_classes = (uint32_t)all.vm["csoaa"].as<size_t>();
  c.pred = calloc_or_die<polyprediction>(c.num_classes);
  
  learner<csoaa>& l = init_learner(&c, setup_base(all), predict_or_learn<true>, 
				   predict_or_learn<false>, c.num_classes);
  all.p->lp = cs_label;
  l.set_finish_example(finish_example);
  l.set_finish(finish);
  base_learner* b = make_base(l);
  all.cost_sensitive = b;
  return b;
}

struct score {
  float val;
  size_t idx;
};

struct ldf {
  v_array<example*> ec_seq;
  LabelDict::label_feature_map label_features;  
  
  size_t read_example_this_loop;
  bool need_to_clear;
  bool is_wap;
  bool first_pass;
  bool treat_as_classifier;
  bool is_singleline;
  float csoaa_example_t;
  vw* all;
  
  bool rank;
  v_array<score> scores;
  
  v_array<MULTILABEL::labels> stored_preds;
  base_learner* base;
};

int score_comp(const void* p1, const void* p2) {
  score* s1 = (score*)p1;
  score* s2 = (score*)p2;
  if(s2->val == s1->val) return 0;
  else if(s2->val >= s1->val) return -1;
  else return 1;
}

  bool ec_is_label_definition(example& ec) // label defs look like "0:___" or just "label:___"
  {
    if (ec.indices.size() != 1) return false;
    if (ec.indices[0] != 'l') return false;
    v_array<COST_SENSITIVE::wclass> costs = ec.l.cs.costs;
    for (size_t j=0; j<costs.size(); j++)
      if ((costs[j].class_index != 0) || (costs[j].x <= 0.)) return false;
    return true;    
  }

  bool ec_seq_is_label_definition(v_array<example*>ec_seq)
  {
    if (ec_seq.size() == 0) return false;
    bool is_lab = ec_is_label_definition(*ec_seq[0]);
    for (size_t i=1; i<ec_seq.size(); i++) {
      if (is_lab != ec_is_label_definition(*ec_seq[i])) {
        if (!((i == ec_seq.size()-1) && (example_is_newline(*ec_seq[i])))) 
	  THROW("error: mixed label definition and examples in ldf data!");
      }
    }
    return is_lab;
  }

inline bool cmp_wclass_ptr(const COST_SENSITIVE::wclass* a, const COST_SENSITIVE::wclass* b) { return a->x < b->x; }

void compute_wap_values(vector<COST_SENSITIVE::wclass*> costs) {
  std::sort(costs.begin(), costs.end(), cmp_wclass_ptr);
  costs[0]->wap_value = 0.;
  for (size_t i=1; i<costs.size(); i++)
    costs[i]->wap_value = costs[i-1]->wap_value + (costs[i]->x - costs[i-1]->x) / (float)i;
}

// Substract a given feature from example ec.
// Rather than finding the corresponding namespace and feature in ec,
// add a new feature with opposite value (but same index) to ec to a special wap_ldf_namespace.
// This is faster and allows fast undo in unsubtract_example().
void subtract_feature(example& ec, float feature_value_x, uint32_t weight_index)
{
  feature temp = { -feature_value_x, weight_index };
  ec.atomics[wap_ldf_namespace].push_back(temp);
  ec.sum_feat_sq[wap_ldf_namespace] += feature_value_x * feature_value_x;
}

// Iterate over all features of ecsub including quadratic and cubic features and subtract them from ec.
void subtract_example(vw& all, example *ec, example *ecsub)
{
  ec->sum_feat_sq[wap_ldf_namespace] = 0;
  GD::foreach_feature<example&, uint32_t, subtract_feature>(all, *ecsub, *ec);
  ec->indices.push_back(wap_ldf_namespace);
  ec->num_features += ec->atomics[wap_ldf_namespace].size();
  ec->total_sum_feat_sq += ec->sum_feat_sq[wap_ldf_namespace];
}

void unsubtract_example(example *ec)
{
  if (ec->indices.size() == 0) {
    cerr << "internal error (bug): trying to unsubtract_example, but there are no namespaces!" << endl;
    return;
  }
    
  if (ec->indices.last() != wap_ldf_namespace) {
    cerr << "internal error (bug): trying to unsubtract_example, but either it wasn't added, or something was added after and not removed!" << endl;
    return;
  }

  ec->num_features -= ec->atomics[wap_ldf_namespace].size();
  ec->total_sum_feat_sq -= ec->sum_feat_sq[wap_ldf_namespace];
  ec->sum_feat_sq[wap_ldf_namespace] = 0;
  ec->atomics[wap_ldf_namespace].erase();
  ec->indices.decr();
}

void make_single_prediction(ldf& data, base_learner& base, example& ec) {
  COST_SENSITIVE::label ld = ec.l.cs;
  label_data simple_label;
  simple_label.initial = 0.;
  simple_label.label = FLT_MAX;
  simple_label.weight = 0.;
  ec.partial_prediction = 0.;
    
  LabelDict::add_example_namespace_from_memory(data.label_features, ec, ld.costs[0].class_index, data.all->audit || data.all->hash_inv);
    
  ec.l.simple = simple_label;
  base.predict(ec); // make a prediction
  ld.costs[0].partial_prediction = ec.partial_prediction;

  LabelDict::del_example_namespace_from_memory(data.label_features, ec, ld.costs[0].class_index, data.all->audit || data.all->hash_inv);
  ec.l.cs = ld;
}

bool check_ldf_sequence(ldf& data, size_t start_K)
{
  bool isTest = COST_SENSITIVE::example_is_test(*data.ec_seq[start_K]);
  for (size_t k=start_K; k<data.ec_seq.size(); k++) {
    example *ec = data.ec_seq[k];
      
    // Each sub-example must have just one cost
    assert(ec->l.cs.costs.size()==1);
      
    if (COST_SENSITIVE::example_is_test(*ec) != isTest) {
      isTest = true;
      cerr << "warning: ldf example has mix of train/test data; assuming test" << endl;
    }
    if (ec_is_example_header(*ec))
      THROW("warning: example headers at position " << k << ": can only have in initial position!");
  }
  return isTest;
}

void do_actual_learning_wap(ldf& data, base_learner& base, size_t start_K)
{
  size_t K = data.ec_seq.size();
  vector<COST_SENSITIVE::wclass*> all_costs;
  for (size_t k=start_K; k<K; k++)
    all_costs.push_back(&data.ec_seq[k]->l.cs.costs[0]);
  compute_wap_values(all_costs);

  data.csoaa_example_t += 1.;
  for (size_t k1=start_K; k1<K; k1++) {
    example *ec1 = data.ec_seq[k1];

    // save original variables
    COST_SENSITIVE::label   save_cs_label = ec1->l.cs;
    label_data& simple_label = ec1->l.simple;
    float save_example_t1 = ec1->example_t;

    v_array<COST_SENSITIVE::wclass> costs1 = save_cs_label.costs;
    if (costs1[0].class_index == (uint32_t)-1) continue;
      
    LabelDict::add_example_namespace_from_memory(data.label_features, *ec1, costs1[0].class_index, data.all->audit || data.all->hash_inv);
      
    for (size_t k2=k1+1; k2<K; k2++) {
      example *ec2 = data.ec_seq[k2];
      v_array<COST_SENSITIVE::wclass> costs2 = ec2->l.cs.costs;
        
      if (costs2[0].class_index == (uint32_t)-1) continue;
      float value_diff = fabs(costs2[0].wap_value - costs1[0].wap_value);
      //float value_diff = fabs(costs2[0].x - costs1[0].x);
      if (value_diff < 1e-6)
        continue;
        
      LabelDict::add_example_namespace_from_memory(data.label_features, *ec2, costs2[0].class_index, data.all->audit || data.all->hash_inv);
        
      // learn
      ec1->example_t = data.csoaa_example_t;
      simple_label.initial = 0.;
      simple_label.label = (costs1[0].x < costs2[0].x) ? -1.0f : 1.0f;
      simple_label.weight = value_diff;
      ec1->partial_prediction = 0.;
      subtract_example(*data.all, ec1, ec2);
      base.learn(*ec1);
      unsubtract_example(ec1);
        
      LabelDict::del_example_namespace_from_memory(data.label_features, *ec2, costs2[0].class_index, data.all->audit || data.all->hash_inv);
    }
    LabelDict::del_example_namespace_from_memory(data.label_features, *ec1, costs1[0].class_index, data.all->audit || data.all->hash_inv);
      
    // restore original cost-sensitive label, sum of importance weights
    ec1->l.cs = save_cs_label;
    ec1->example_t = save_example_t1;
    // TODO: What about partial_prediction? See do_actual_learning_oaa.
  }
}

void do_actual_learning_oaa(ldf& data, base_learner& base, size_t start_K)
{
  size_t K = data.ec_seq.size();
  float  min_cost  = FLT_MAX;
  float  max_cost  = -FLT_MAX;

  for (size_t k=start_K; k<K; k++) {
    float ec_cost = data.ec_seq[k]->l.cs.costs[0].x;
    if (ec_cost < min_cost) min_cost = ec_cost;
    if (ec_cost > max_cost) max_cost = ec_cost;
  }

  data.csoaa_example_t += 1.;
  for (size_t k=start_K; k<K; k++) {
    example *ec = data.ec_seq[k];
      
    // save original variables
    label save_cs_label = ec->l.cs;
    float save_example_t = ec->example_t;
    v_array<COST_SENSITIVE::wclass> costs = save_cs_label.costs;

    // build example for the base learner
    label_data simple_label;
    ec->example_t = data.csoaa_example_t;
      
    simple_label.initial = 0.;
    simple_label.weight = 1.;
    if (!data.treat_as_classifier) { // treat like regression
      simple_label.label = costs[0].x;
    } else { // treat like classification
      if (costs[0].x <= min_cost) {
        simple_label.label = -1.;
        simple_label.weight = max_cost - min_cost;
      } else {
        simple_label.label = 1.;
        simple_label.weight = costs[0].x - min_cost;
      }
    }
    ec->l.simple = simple_label;

    // learn
    LabelDict::add_example_namespace_from_memory(data.label_features, *ec, costs[0].class_index, data.all->audit || data.all->hash_inv);
    base.learn(*ec);
    LabelDict::del_example_namespace_from_memory(data.label_features, *ec, costs[0].class_index, data.all->audit || data.all->hash_inv);
      
    // restore original cost-sensitive label, sum of importance weights and partial_prediction
    ec->l.cs = save_cs_label;
    ec->example_t = save_example_t;
    ec->partial_prediction = costs[0].partial_prediction;
  }
}

template <bool is_learn>
void do_actual_learning(ldf& data, base_learner& base)
{
  //cout<< "do_actual_learning size=" << data.ec_seq.size() << endl;
  if (data.ec_seq.size() <= 0) return;  // nothing to do
  
  /////////////////////// handle label definitions
  if (ec_seq_is_label_definition(data.ec_seq)) {
    for (size_t i=0; i<data.ec_seq.size(); i++) {
      v_array<feature> features = v_init<feature>();
      v_array<audit_data> audit = v_init<audit_data>();
      for (feature*f=data.ec_seq[i]->atomics[data.ec_seq[i]->indices[0]].begin; f!=data.ec_seq[i]->atomics[data.ec_seq[i]->indices[0]].end; f++) {
        feature fnew = { f->x,  f->weight_index };
        features.push_back(fnew);
      }
      if ((data.all->audit || data.all->hash_inv))
        for (audit_data*f=data.ec_seq[i]->audit_features[data.ec_seq[i]->indices[0]].begin; f!=data.ec_seq[i]->audit_features[data.ec_seq[i]->indices[0]].end; f++) {
          audit_data f2 = { f->space, f->feature, f->weight_index, f->x, false };
          audit.push_back(f2);
        }

      v_array<COST_SENSITIVE::wclass>& costs = data.ec_seq[i]->l.cs.costs;
      for (size_t j=0; j<costs.size(); j++) {
        size_t lab = (size_t)costs[j].x;
        LabelDict::set_label_features(data.label_features, lab, features, (data.all->audit || data.all->hash_inv) ? &audit : nullptr);
      }
    }
    return;
  }

  /////////////////////// add headers
  size_t K = data.ec_seq.size();
  size_t start_K = 0;

  if (ec_is_example_header(*data.ec_seq[0])) {
    start_K = 1;
    for (size_t k=1; k<K; k++)
      LabelDict::add_example_namespaces_from_example(*data.ec_seq[k], *data.ec_seq[0], (data.all->audit || data.all->hash_inv));
  }
  bool isTest = check_ldf_sequence(data, start_K);

  /////////////////////// do prediction
  size_t predicted_K = start_K;
  if(data.rank) {
    data.scores.erase();
    data.stored_preds.erase();
    if (start_K > 0)
      data.stored_preds.push_back(data.ec_seq[0]->pred.multilabels);
    
    for (size_t k=start_K; k<K; k++) {
      data.stored_preds.push_back(data.ec_seq[k]->pred.multilabels);
      example *ec = data.ec_seq[k];      
      make_single_prediction(data, base, *ec);
      score s;
      s.val = ec->partial_prediction;
      s.idx = k - start_K;
      data.scores.push_back(s);
    }    

    qsort((void*) data.scores.begin, data.scores.size(), sizeof(score), score_comp);        
  }
  else {
    float  min_score = FLT_MAX;       
    for (size_t k=start_K; k<K; k++) {
      example *ec = data.ec_seq[k];
      make_single_prediction(data, base, *ec);
      if (ec->partial_prediction < min_score) {
	min_score = ec->partial_prediction;
	predicted_K = k;
      }
    }   
  }
  

  /////////////////////// learn
  if (is_learn && !isTest){
    if (data.is_wap) do_actual_learning_wap(data, base, start_K);
    else             do_actual_learning_oaa(data, base, start_K);
  }

  
  if(data.rank) {
    data.stored_preds[0].label_v.erase();
    if (start_K > 0) {
      data.ec_seq[0]->pred.multilabels = data.stored_preds[0];
    }
    for (size_t k=start_K; k<K; k++) {
      data.ec_seq[k]->pred.multilabels = data.stored_preds[k];
      data.ec_seq[0]->pred.multilabels.label_v.push_back(data.scores[k-start_K].idx);
    }
  }  
  else // Mark the predicted subexample with its class_index, all other with 0
    for (size_t k=start_K; k<K; k++)
      data.ec_seq[k]->pred.multiclass = (k == predicted_K) ? data.ec_seq[k]->l.cs.costs[0].class_index : 0;
  
  /////////////////////// remove header
  if (start_K > 0)
    for (size_t k=1; k<K; k++)
      LabelDict::del_example_namespaces_from_example(*data.ec_seq[k], *data.ec_seq[0], (data.all->audit || data.all->hash_inv));
}

void global_print_newline(vw& all)
{
  char temp[1];
  temp[0] = '\n';
  for (size_t i=0; i<all.final_prediction_sink.size(); i++) {
    int f = all.final_prediction_sink[i];
    ssize_t t;
    t = io_buf::write_file_or_socket(f, temp, 1);
    if (t != 1)
      cerr << "write error: " << strerror(errno) << endl;
  }
}

void output_example(vw& all, example& ec, bool& hit_loss, v_array<example*>* ec_seq)
{
  label& ld = ec.l.cs;
  v_array<COST_SENSITIVE::wclass> costs = ld.costs;
    
  if (example_is_newline(ec)) return;
  if (ec_is_example_header(ec)) return;
  if (ec_is_label_definition(ec)) return;

  all.sd->total_features += ec.num_features;

  float loss = 0.;

  if (!COST_SENSITIVE::example_is_test(ec)) {
    for (size_t j=0; j<costs.size(); j++) {
      if (hit_loss) break;
      if (ec.pred.multiclass == costs[j].class_index) {
        loss = costs[j].x;
        hit_loss = true;
      }
    }

    all.sd->sum_loss += loss;
    all.sd->sum_loss_since_last_dump += loss;
    assert(loss >= 0);
  }
  
  for (int* sink = all.final_prediction_sink.begin; sink != all.final_prediction_sink.end; sink++)
    all.print(*sink, (float)ec.pred.multiclass, 0, ec.tag);

  if (all.raw_prediction > 0) {
    string outputString;
    stringstream outputStringStream(outputString);
    for (size_t i = 0; i < costs.size(); i++) {
      if (i > 0) outputStringStream << ' ';
      outputStringStream << costs[i].class_index << ':' << costs[i].partial_prediction;
    }
    //outputStringStream << endl;
    all.print_text(all.raw_prediction, outputStringStream.str(), ec.tag);
  }
    
  COST_SENSITIVE::print_update(all, COST_SENSITIVE::example_is_test(ec), ec, ec_seq);
}

void output_rank_example(vw& all, example& head_ec, bool& hit_loss, v_array<example*>* ec_seq)
{
  label& ld = head_ec.l.cs;
  v_array<COST_SENSITIVE::wclass> costs = ld.costs;
  
  if (example_is_newline(head_ec)) return;
  if (ec_is_label_definition(head_ec)) return;
  
  all.sd->total_features += head_ec.num_features;
  
  float loss = 0.;
  v_array<uint32_t> preds = head_ec.pred.multilabels.label_v;
  
  if (!COST_SENSITIVE::example_is_test(head_ec)) {
    size_t idx = 0;
    for(example** ecc = ec_seq->begin; ecc != ec_seq->end;ecc++,idx++) {
      example& ex = **ecc;
      if(ec_is_example_header(ex)) continue;
      if (hit_loss) break;
      if (preds[0] == idx) {
	loss = ex.l.cs.costs[0].x;
	hit_loss = true;
      }
    }

    all.sd->sum_loss += loss;
    all.sd->sum_loss_since_last_dump += loss;
    assert(loss >= 0);
  }
  
  for (int* sink = all.final_prediction_sink.begin; sink != all.final_prediction_sink.end; sink++)
    MULTILABEL::print_multilabel(*sink, head_ec.pred.multilabels, head_ec.tag);
  
  if (all.raw_prediction > 0) {
    string outputString;
    stringstream outputStringStream(outputString);
    for (size_t i = 0; i < costs.size(); i++) {
      if (i > 0) outputStringStream << ' ';
      outputStringStream << costs[i].class_index << ':' << costs[i].partial_prediction;
    }
    //outputStringStream << endl;
    all.print_text(all.raw_prediction, outputStringStream.str(), head_ec.tag);
  }
  
  COST_SENSITIVE::print_update(all, COST_SENSITIVE::example_is_test(head_ec), head_ec, ec_seq, true);
}

void output_example_seq(vw& all, ldf& data)
{
  if ((data.ec_seq.size() > 0) && !ec_seq_is_label_definition(data.ec_seq)) {
    all.sd->weighted_examples += 1;
    all.sd->example_number++;

    bool hit_loss = false;
    if(data.rank)
      output_rank_example(all, **(data.ec_seq.begin), hit_loss, &(data.ec_seq));
    else
      for (example** ecc=data.ec_seq.begin; ecc!=data.ec_seq.end; ecc++)
	output_example(all, **ecc, hit_loss, &(data.ec_seq));
    
    if (!data.is_singleline && (all.raw_prediction > 0)) {
      v_array<char> empty = { nullptr, nullptr, nullptr, 0 };
      all.print_text(all.raw_prediction, "", empty);
    }
  }
}

void clear_seq_and_finish_examples(vw& all, ldf& data)
{
  if (data.ec_seq.size() > 0) 
    for (example** ecc=data.ec_seq.begin; ecc!=data.ec_seq.end; ecc++)
      if ((*ecc)->in_use)
        VW::finish_example(all, *ecc);
  data.ec_seq.erase();
}

void end_pass(ldf& data)
{
  data.first_pass = false;
}

void finish_singleline_example(vw& all, ldf&, example& ec)
{
  if (! ec_is_label_definition(ec)) {
    all.sd->weighted_examples += 1;
    all.sd->example_number++;
  }
  bool hit_loss = false;
  output_example(all, ec, hit_loss, nullptr);
  VW::finish_example(all, &ec);
}

void finish_multiline_example(vw& all, ldf& data, example& ec)
{
  if (data.need_to_clear) {
    if (data.ec_seq.size() > 0) {
      output_example_seq(all, data);
      global_print_newline(all);
    }        
    clear_seq_and_finish_examples(all, data);
    data.need_to_clear = false;
    if (ec.in_use) VW::finish_example(all, &ec);
  }
}

void end_examples(ldf& data)
{
  if (data.need_to_clear)
    data.ec_seq.erase();
}


void finish(ldf& data)
{
  data.ec_seq.delete_v();
  LabelDict::free_label_features(data.label_features);
  data.scores.delete_v();
  data.stored_preds.delete_v();
}

template <bool is_learn>
void predict_or_learn(ldf& data, base_learner& base, example &ec) {
  vw* all = data.all;
  data.base = &base;
  bool is_test_ec = COST_SENSITIVE::example_is_test(ec);
  bool need_to_break = data.ec_seq.size() >= all->p->ring_size - 2;

  // singleline is used by library/ezexample_predict
  if (data.is_singleline) {
    assert(is_test_ec); // Only test examples are supported with singleline
    assert(ec.l.cs.costs.size() > 0); // headers not allowed with singleline
    make_single_prediction(data, base, ec);
  } else if (ec_is_label_definition(ec)) {
    if (data.ec_seq.size() > 0) 
      THROW("error: label definition encountered in data block");

    data.ec_seq.push_back(&ec);
    do_actual_learning<is_learn>(data, base);
    data.need_to_clear = true;
  } else if ((example_is_newline(ec) && is_test_ec) || need_to_break) {
    if (need_to_break && data.first_pass)
      cerr << "warning: length of sequence at " << ec.example_counter << " exceeds ring size; breaking apart" << endl;
    do_actual_learning<is_learn>(data, base);
    data.need_to_clear = true;
  } else {
    if (data.need_to_clear) {  // should only happen if we're NOT driving
      data.ec_seq.erase();
      data.need_to_clear = false;
    }
    data.ec_seq.push_back(&ec);
  }
}

base_learner* csldf_setup(vw& all)
{
  if (missing_option<string, true>(all, "csoaa_ldf", "Use one-against-all multiclass learning with label dependent features.  Specify singleline or multiline.")
      && missing_option<string, true>(all, "wap_ldf", "Use weighted all-pairs multiclass learning with label dependent features.  Specify singleline or multiline."))
    return nullptr;
  new_options(all, "LDF Options")
      ("ldf_override", po::value<string>(), "Override singleline or multiline from csoaa_ldf or wap_ldf, eg if stored in file")
    ("csoaa_rank","Return actions sorted by score order");
  add_options(all);

  po::variables_map& vm = all.vm;
  ldf& ld = calloc_or_die<ldf>();

  ld.all = &all;
  ld.need_to_clear = true;
  ld.first_pass = true;
 
  string ldf_arg;

  if( vm.count("csoaa_ldf") ){
    ldf_arg = vm["csoaa_ldf"].as<string>();
  }
  else {
    ldf_arg = vm["wap_ldf"].as<string>();
    ld.is_wap = true;
  }
  if ( vm.count("ldf_override") )
    ldf_arg = vm["ldf_override"].as<string>();
  if (vm.count("csoaa_rank"))
    {
      ld.rank = true;
      all.multilabel_prediction = true;
    }

  all.p->lp = COST_SENSITIVE::cs_label;

  ld.treat_as_classifier = false;
  ld.is_singleline = false;
  if (ldf_arg.compare("multiline") == 0 || ldf_arg.compare("m") == 0) {
    ld.treat_as_classifier = false;
  } else if (ldf_arg.compare("multiline-classifier") == 0 || ldf_arg.compare("mc") == 0) {
    ld.treat_as_classifier = true;
  } else {
    if (all.training) 
      THROW("ldf requires either m/multiline or mc/multiline-classifier, except in test-mode which can be s/sc/singleline/singleline-classifier");

    if (ldf_arg.compare("singleline") == 0 || ldf_arg.compare("s") == 0) {
      ld.treat_as_classifier = false;
      ld.is_singleline = true;
    } else if (ldf_arg.compare("singleline-classifier") == 0 || ldf_arg.compare("sc") == 0) {
      ld.treat_as_classifier = true;
      ld.is_singleline = true;
    }
  }

  all.p->emptylines_separate_examples = true; // TODO: check this to be sure!!!  !ld.is_singleline;

  /*if (all.add_constant) {
    all.add_constant = false;
    }*/
  v_array<feature> empty_f = { nullptr, nullptr, nullptr, 0 };
  v_array<audit_data> empty_a = { nullptr, nullptr, nullptr, 0 };
  LabelDict::feature_audit empty_fa = { empty_f, empty_a };
  ld.label_features.init(256, empty_fa, LabelDict::size_t_eq);
  ld.label_features.get(1, 94717244); // TODO: figure this out

  ld.read_example_this_loop = 0;
  ld.need_to_clear = false;
  learner<ldf>& l = init_learner(&ld, setup_base(all), predict_or_learn<true>, predict_or_learn<false>);
  if (ld.is_singleline)
    l.set_finish_example(finish_singleline_example);
  else
    l.set_finish_example(finish_multiline_example);
  l.set_finish(finish);
  l.set_end_examples(end_examples); 
  l.set_end_pass(end_pass);
  return make_base(l);
}
