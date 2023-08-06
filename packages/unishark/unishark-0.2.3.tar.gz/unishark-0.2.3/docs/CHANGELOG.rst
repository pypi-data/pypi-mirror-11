CHANGELOG
=========

0.2.3 (2015-09-01)
------------------

 - enable 'module' and 'method' level concurrent execution in a suite.


0.2.2 (2015-08-12)
------------------

 - support loading tests from a package with pattern matching, and excluding modules/classes/methods from the loaded tests.
 - add load_tests_from_package and load_tests_from_modules api.
 - rename load_test_from_dict to load_tests_from_dict.
 - fix that verbose stdout mode does not print test method doc string.
 - fix that tests loaded with method granularity are not filtered by method name pattern.
 - less strict dependency versions.


0.2.1 (2015-05-11)
------------------

 - support data-driven with multi-threads.


0.2.0 (2015-04-04)
------------------

 - support running tests in parallel.

 - support configuring test suites, test reporters and concurrent tests in a single dict/yaml config.

 - improve HtmlReporter and XUnitReporter classes to be thread-safe.

 - allow user to generate reports with their own report templates.

 - allow user to filter loaded test cases by setting method name prefix in the test config.

 - bugs fix.

 - improve documentation.


0.1.2 (2015-03-25)
------------------

 - hotfix for setup.py (broken auto-downloading dependencies)

 - bugs fix.


0.1.1 (2015-03-24)
------------------

 - support loading customized test suites.

 - support a thread-safe string io buffer to buffer logging stream during the test running.

 - support writing logs, exceptions into generated HTML/XUnit reports.

 - offer a data-driven decorator.

 - initial setup (documentation, setup.py, travis CI, coveralls, etc.).
