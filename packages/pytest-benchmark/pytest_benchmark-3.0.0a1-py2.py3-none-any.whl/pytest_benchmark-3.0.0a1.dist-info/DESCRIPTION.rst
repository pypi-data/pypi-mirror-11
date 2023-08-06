================
pytest-benchmark
================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires| |coveralls| |codecov|
        | |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pytest-benchmark/badge/?style=flat
    :target: https://readthedocs.org/projects/pytest-benchmark
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/pytest-benchmark.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/pytest-benchmark

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/pytest-benchmark?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/pytest-benchmark

.. |requires| image:: https://requires.io/github/ionelmc/pytest-benchmark/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/pytest-benchmark/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/pytest-benchmark/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/pytest-benchmark

.. |codecov| image:: https://codecov.io/github/ionelmc/pytest-benchmark/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/pytest-benchmark

.. |landscape| image:: https://landscape.io/github/ionelmc/pytest-benchmark/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/pytest-benchmark/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/80e2960677c24d5083a802dd57df17dc.svg?style=flat
    :target: https://www.codacy.com/app/ionelmc/pytest-benchmark
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/ionelmc/pytest-benchmark/badges/gpa.svg
   :target: https://codeclimate.com/github/ionelmc/pytest-benchmark
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/pytest-benchmark.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pytest-benchmark

.. |downloads| image:: https://img.shields.io/pypi/dm/pytest-benchmark.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pytest-benchmark

.. |wheel| image:: https://img.shields.io/pypi/wheel/pytest-benchmark.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pytest-benchmark

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytest-benchmark.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pytest-benchmark

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pytest-benchmark.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pytest-benchmark

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/pytest-benchmark/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/pytest-benchmark/

A ``py.test`` fixture for benchmarking code. It will group the tests into rounds that are calibrated to the chosen
timer. See calibration_ and FAQ_.

* Free software: BSD license

Installation
============

::

    pip install pytest-benchmark

Documentation
=============

`pytest-benchmark.readthedocs.org <http://pytest-benchmark.readthedocs.org/en/stable/>`_

Examples
========

This plugin provides a `benchmark` fixture. This fixture is a callable object that will benchmark
any function passed to it.

Example:

.. code-block:: python

    def something(duration=0.000001):
        # Code to be measured
        return time.sleep(duration)

    def test_my_stuff(benchmark):
        # benchmark something
        result = benchmark(something)

        # Extra code, to verify that the run completed correctly.
        # Note: this code is not measured.
        assert result is None

You can also pass extra arguments:

.. code-block:: python

    def test_my_stuff(benchmark):
        result = benchmark(time.sleep, 0.02)


Screenshots
-----------

Normal run:

.. image:: https://github.com/ionelmc/pytest-benchmark/raw/master/docs/screenshot.png
    :alt: Screenshot of py.test summary

Compare mode (``--benchmark-compare``):

.. image:: https://github.com/ionelmc/pytest-benchmark/raw/master/docs/screenshot-compare.png
    :alt: Screenshot of py.test summary in compare mode

Histogram (``--benchmark-histogram``):

.. image:: https://cdn.rawgit.com/ionelmc/pytest-benchmark/94860cc8f47aed7ba4f9c7e1380c2195342613f6/docs/sample-tests_test_normal.py_test_xfast_parametrized%5B0%5D.svg
    :alt: Histogram sample

..

    Also, it has `nice tooltips
    <https://cdn.rawgit.com/ionelmc/pytest-benchmark/94860cc8f47aed7ba4f9c7e1380c2195342613f6/docs/sample-tests_test_normal.py_test_xfast_parametrized%5B0%5D.svg>`_.

Development
===========

To run the all tests run::

    tox

Credits
=======

* Timing code and ideas taken from: https://bitbucket.org/haypo/misc/src/tip/python/benchmark.py

.. _FAQ: http://pytest-benchmark.readthedocs.org/en/latest/faq.html
.. _calibration: http://pytest-benchmark.readthedocs.org/en/latest/features.html#calibration







Changelog
=========

3.0.0 (?????????)
-----------------

* Added JSON report saving (the ``--benchmark-json`` command line arguments).
* Added benchmark data storage(the ``--benchmark-save`` and ``--benchmark-autosave`` command line arguments).
* Added comparison to previous runs (the ``--benchmark-compare`` command line argument).
* Added performance regression checks (the ``--benchmark-compare-fail`` command line argument).
* Added possibility to group by various parts of test name (the `--benchmark-compare-group-by`` command line argument).
* Added historical plotting (the ``--benchmark-histogram`` command line argument).
* Added option to fine tune the calibration (the ``--benchmark-calibration-precision`` command line argument and
  ``calibration_precision`` marker option).

* Changed ``benchmark_weave`` to no longer be a context manager. Cleanup is performed automatically. *BACKWARDS INCOMPATIBLE*
* Added ``benchmark.weave`` method (alternative to ``benchmark_weave`` fixture).

* Added new hooks to allow customization:

  * ``pytest_benchmark_generate_machine_info(config)``
  * ``pytest_benchmark_update_machine_info(config, info)``
  * ``pytest_benchmark_generate_commit_info(config)``
  * ``pytest_benchmark_update_commit_info(config, info)``
  * ``pytest_benchmark_group_stats(config, benchmarks, group_by)``
  * ``pytest_benchmark_generate_json(config, benchmarks, include_data)``
  * ``pytest_benchmark_update_json(config, benchmarks, output_json)``
  * ``pytest_benchmark_compare_machine_info(config, benchmarksession, machine_info, compared_benchmark)``

* Changed the timing code to:

  * Tracers are automatically disabled when running the test function (like coverage tracers).
  * Fixed an issue with calibration code getting stuck.

* Added `pedantic mode` via ``benchmark.pedantic()``. This mode disables calibration and allows a setup function.


2.5.0 (2015-06-20)
------------------

* Improved test suite a bit (not using `cram` anymore).
* Improved help text on the ``--benchmark-warmup`` option.
* Made ``warmup_iterations`` available as a marker argument (eg: ``@pytest.mark.benchmark(warmup_iterations=1234)``).
* Fixed ``--benchmark-verbose``'s printouts to work properly with output capturing.
* Changed how warmup iterations are computed (now number of total iterations is used, instead of just the rounds).
* Fixed a bug where calibration would run forever.
* Disabled red/green coloring (it was kinda random) when there's a single test in the results table.

2.4.1 (2015-03-16)
------------------

* Fix regression, plugin was raising ``ValueError: no option named 'dist'`` when xdist wasn't installed.

2.4.0 (2015-03-12)
------------------

* Add a ``benchmark_weave`` experimental fixture.
* Fix internal failures when `xdist` plugin is active.
* Automatically disable benchmarks if `xdist` is active.

2.3.0 (2014-12-27)
------------------

* Moved the warmup in the calibration phase. Solves issues with benchmarking on PyPy.

  Added a ``--benchmark-warmup-iterations`` option to fine-tune that.

2.2.0 (2014-12-26)
------------------

* Make the default rounds smaller (so that variance is more accurate).
* Show the defaults in the ``--help`` section.

2.1.0 (2014-12-20)
------------------

* Simplify the calibration code so that the round is smaller.
* Add diagnostic output for calibration code (``--benchmark-verbose``).

2.0.0 (2014-12-19)
------------------

* Replace the context-manager based API with a simple callback interface. *BACKWARDS INCOMPATIBLE*
* Implement timer calibration for precise measurements.

1.0.0 (2014-12-15)
------------------

* Use a precise default timer for PyPy.

? (?)
-----

* Readme and styling fixes (contributed by Marc Abramowitz)
* Lots of wild changes.


