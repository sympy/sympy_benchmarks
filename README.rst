SymPy's benchmark suite
=======================

.. image:: http://img.shields.io/badge/benchmarked%20by-asv-green.svg?style=flat
   :target: http://hera.physchem.kth.se/~sympy_asv
   :alt: airspeedvelocity

.. image:: https://travis-ci.org/sympy/sympy_benchmarks.png?branch=master
   :target: https://travis-ci.org/sympy/sympy_benchmarks


This is the benchmark suite for `SymPy <http://github.com/sympy/sympy>`__.

These benchmarks track the performance of various features in SymPy
*over time*.

Results are currently hosted in an ad hoc manner, you may find some results `here
<http://hera.physchem.kth.se/~sympy_asv>`__ and `here <http://www.moorepants.info/misc/sympy-asv/>`__.

The benchmarks are run using `airspeed velocity
<https://asv.readthedocs.io/>`__.

When adding benchmarks, mirror the SymPy directory tree for the feature you are
adding. If your benchmark is not for a specific feature such that creating
subdirectories for your benchmark is not reasonable, put your benchmark in the
top level benchmarking directory.


Quickstart
----------

Installation
^^^^^^^^^^^^

Firstly, you need to install ``asv``

``pip install asv``

or in conda environment, use

``conda install -c conda-forge asv``

And then you may also need to install ``virtualenv``. Because we have
``"environment_type": "virtualenv"`` in ``asf.conf.json``.

``pip install virtualenv``

or in conda environment, use

``conda install -c conda-forge virtualenv`` to install the dependency.

Running the benchmarks
^^^^^^^^^^^^^^^^^^^^^^

Use ``asv run`` command to run the benchmarks.

Or alternatively, you may use ``asv run --quick`` to try out the benchmarks
quickly, if it is slow.

You may also use ``asv run --bench <Name>`` to selectively run a specific
benchmark based on the function or class name in ``benchmarks/`` or
``slow_benchmarks/`` folder. It also supports regular expressions.

The benchmark results will be stored in your ``reports/`` folder.

See `asv documentation <https://asv.readthedocs.io/en/stable/commands.html#asv-run>`__
for additional information.

Creating and viewing the HTML report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``asv publish`` command to create an HTML report.

It will generate an HTML report in your ``html/`` folder. However, you may
not be able to use the HTML files directly.

After generating the HTML files, you have to use ``asv preview`` to create
a server locally. And navigate to ``http://127.0.0.1:8080/`` to view the
report.

See `asv documentation <https://asv.readthedocs.io/en/stable/commands.html#asv-publish>`__
for additional information.
