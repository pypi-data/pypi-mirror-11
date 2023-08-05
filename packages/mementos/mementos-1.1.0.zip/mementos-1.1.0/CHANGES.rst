
Change Log
==========

1.0.6 (August 4, 2015)
''''''''''''''''''''''

 * Switched to Apache Software License 2.0.
 * Updated testing configuration to add 3.5 and tox improvements.
 * Added wheel software packaging.

1.0.5 (July 22, 2015)
'''''''''''''''''''''

 * Inagurated continuous integration testing with Travis CI.

1.0.4 (May 14, 2005)
''''''''''''''''''''

 * Updated testing to include 3.5a4 and most recent versions of PyPy
   and PyPy3. Tweaks to docs.

1.0.3 (December 30, 2014)
'''''''''''''''''''''''''

 * Tweaked documentation. Reran tests on latest versions.
   Withdrew support for Python 2.5, which
   is no longer supported by my testing tools.

1.0
'''

  * Cleaned up source for better PEP8 conformance
  * Bumped version number to 1.0 as part of move to `semantic
    versioning <http://semver.org>`_, or at least enough of it so
    as to not screw up Python installation procedures (which don't
    seem to understand 0.401 is a lesser version that 0.5, because
    401 > 5).
