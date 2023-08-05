# Setuptools Green

This module provides a "green" command for setuptools scripts that uses
[green](https://github.com/CleanCut/green) to run tests.

## Status

| Travis CI (Ubuntu) | AppVeyor (Windows) | Coverage | PyPI | Licence |
|--------------------|--------------------|----------|------|---------|
|[![Travis](https://img.shields.io/travis/polysquare/jobstamps.svg)](http://travis-ci.org/polysquare/jobstamps)|[![AppVeyor](https://img.shields.io/appveyor/ci/smspillaz/jobstamps.svg)](https://ci.appveyor.com/project/smspillaz/jobstamps)|[![Coveralls](https://img.shields.io/coveralls/polysquare/jobstamps.svg)](http://coveralls.io/polysquare/jobstamps)|[![PyPIVersion](https://img.shields.io/pypi/v/jobstamps.svg)](https://pypi.python.org/pypi/jobstamps)[![PyPIPythons](https://img.shields.io/pypi/pyversions/jobstamps.svg)](https://pypi.python.org/pypi/jobstamps)|[![License](https://img.shields.io/github/license/polysquare/jobstamps.svg)](http://github.com/polysquare/jobstamps)|

## Usage

    Options for 'GreenTestCommand' command:
      --quiet          Don't show test descriptions when running
      --concurrent     Run tests concurrently
      --coverage       Collect coverage
      --coverage-omit  Patterns to omit from coverage, comma separated
      --target         Name of subdirectory where tests are to be found

By default, the verbose mode is used, but you can pass --quiet
to just show dots for passes and "E" for failures.
