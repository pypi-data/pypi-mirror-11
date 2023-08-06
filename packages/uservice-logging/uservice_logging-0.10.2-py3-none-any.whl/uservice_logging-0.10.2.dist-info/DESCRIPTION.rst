uservice-logging
#################

This python library provides logging utilities we use when building
micro-services.

Hacking Notes:
==============

To hack on the library, create a python3 virtual environment with the
development dependencies getting the project pip-cache::

  $ make bootstrap

possibly::

  $ . env/bin/activate

To run the tests::

  $ make test

Dependencies:
=============

setup.py does not list any install-time dependencies, and users of
this library must ensure they have the required dependencies
configured.


