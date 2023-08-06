==================

pytest-wholenodeid will print the entire node id for test failures in the
header.

It turns this::

  =============================================== FAILURES ===============================================
  ______________________________ TriggerRuleMatchTests.test_match_locale _________________________________
  Traceback (most recent call last):
    File "/home/willkg/mozilla/fjord/fjord/suggest/providers/trigger/tests/test_models.py", line 24, in test_match_locale
      for tr_locales, feedback_locale, expected in tests:
  NameError: global name 'tests' is not defined

into this::

  =============================================== FAILURES ===============================================
  ____ fjord/suggest/providers/trigger/tests/test_models.py::TriggerRuleMatchTests::test_match_locale ____
  Traceback (most recent call last):
    File "/home/willkg/mozilla/fjord/fjord/suggest/providers/trigger/tests/test_models.py", line 24, in test_match_locale
      for tr_locales, feedback_locale, expected in tests:
  NameError: global name 'tests' is not defined

Why?

Because then you can copy and paste the node id in the header to more easily
run that specific test.


Quick start
===========

Install::

  $ pip install pytest-wholenodeid

It works by default. If you don't want wholenodeid, then you can pass
``--nowholenodeid`` as an argument to disable it.


Project details
===============

:Code:          https://github.com/willkg/pytest-wholenodeid
:Documentation: You're reading it
:Issue tracker: https://github.com/willkg/pytest-wholenodeid/issues
:License:       Simplified BSD License; see LICENSE file

Home-page: https://github.com/willkg/pytest-wholenodeid
Author: Will Kahn-Greene
Author-email: willkg@bluesock.org
License: Simplified BSD License
Description: UNKNOWN
Keywords: py.test pytest
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Console
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: POSIX
Classifier: Operating System :: POSIX :: Linux
Classifier: Operating System :: Unix
Classifier: Topic :: Software Development :: Testing
Classifier: Topic :: Software Development :: Libraries
Classifier: Topic :: Utilities
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
