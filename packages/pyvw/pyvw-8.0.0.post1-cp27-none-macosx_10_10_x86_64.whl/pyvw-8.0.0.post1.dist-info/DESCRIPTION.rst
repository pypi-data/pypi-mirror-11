PIP Installable version of Vowpal Wabbit.

You need to have boost (libboost-program-options-dev and libboost-python-dev) and python
development packages installed on your system for it to build correctly. See the Vowpal Wabbit
side for more information about building VW.

Since the pyvw wrapper bundled with Vowpal Wabbit links statically to libvw.a this package will
always build it's own library and (currently) cannot use the system installed libvw.so provided
by distribution packages.


