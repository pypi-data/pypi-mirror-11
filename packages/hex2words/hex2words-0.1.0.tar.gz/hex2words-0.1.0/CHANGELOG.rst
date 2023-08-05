.. _changelog:

Changelog
=========

0.1.0 (2015-08-17)
------------------

Second release.

* Modifies output, so all output words will be in lowercase (Issue1_).
* Adds Python 2 support, by Alex Willmer (see PR1_)
* Adds tests
* Adds tox

0.0.1 (2015-06-14)
------------------

Initial protoype.

* Provides hex2words function for use as a library from external apps
* Parses sha1sum output and similar commands (sha512sum, etc.)
* Parses command-line arguments
* Parses *GPG --list-keys* output

.. _Issue1: https://bitbucket.org/pfigue/hex2words/issues/1/output-all-in-lowercase
.. _PR1: https://bitbucket.org/pfigue/hex2words/pull-requests/1/fix-python-2x-and-declare-it-as-supported/
