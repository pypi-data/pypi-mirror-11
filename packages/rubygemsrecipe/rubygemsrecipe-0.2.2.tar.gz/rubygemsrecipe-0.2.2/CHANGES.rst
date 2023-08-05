Change History
**************

0.2.2 (2015-08-18)
==================

- Fix: https://bitbucket.org/sirex/rubygemsrecipe/issues/8/cant-find-latest-rubygems-version (thanks Pierre Allix)

0.2.1 (2014-11-21)
==================

- Fix: https://bitbucket.org/sirex/rubygemsrecipe/issue/6/cannot-install-rubygems-020

0.2.0 (2014-11-20)
==================

- Native Python 2 and Python 3 support using ``six``, without ``use_2to3``.

- Tests for Python 2 and Python 3 using ``tox`` with 100% test coverage.

- All ``subprocess`` commands are rewritten to run without ``shell=True``.

0.1.8 (2014-01-26)
==================

- Feature: Python 3 support.

- Feature: added 'url', 'gem-options' and 'environment' options.

- Fix: add quotes to values of environment variables.

0.1.7 (2012-05-24)
==================

- Feature: added 'ruby-executable' option, thanks to desaintmartin.

0.1.6 (2012-04-26)
==================

- Fix: pass all arguments as separate arguments instead of a single string.

0.1.5 (2012-01-06)
==================

- Fix: use each version only for the line it's specified in.

0.1.4 (2012-01-03)
==================

- You can specify a version for each gem with a syntax similar to python eggs.


0.1.3 (2011-12-28)
==================

- Added 'version' option to specify explicit rubygems version.

0.1.2 (2011-11-09)
==================

- New version of rubygems includes symlinks in .tgz archyve and extracted by
  setuptools.archive_util extractor ignores all symlinks. This causes missing
  files in extracted folder. Now rubygemsrecipe downloads .zip archyve instead
  of .tgz.

0.1.1 (2011-10-04)
==================

- Fixed issue with name of gem executable, which can be different depending on
  how ruby is istalled on host system.

- Install rubygems if gem executable is not found, not rubygems direcotry.

0.1 (2011-09-07)
================

- Initial public release.
