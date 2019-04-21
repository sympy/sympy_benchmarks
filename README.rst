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
