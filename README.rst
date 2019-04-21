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

If you're not using conda, you may also need to install ``virtualenv``.

``pip install virtualenv``


Running the benchmarks
^^^^^^^^^^^^^^^^^^^^^^

To quickly try out the benchmarks (e.g. while developing a new benchmark you can
run it against a single commit on sympy master::

  $ ./run_benchmarks.sh --quick "HEAD^!"

You may also use ``asv run --bench <Name>`` to selectively run a specific
benchmark based on the function or class name in ``benchmarks/`` or
``slow_benchmarks/`` folder. It also supports regular expressions.

The benchmark results will be stored in your ``results/`` folder.

See `asv documentation <https://asv.readthedocs.io/en/stable/commands.html#asv-run>`__
for additional information.

Running benchmarks for a selection of commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generally we're not interested in benchmarking every single commit to the sympy repo.
For example, we might be interested in some tagged releases::

   $ for release in 1.0 1.1 1.2 1.3 1.4; do asv run "sympy-$release^!"; done

or all the merge commits to the master branch since some tag::

   $ git rev-list --merges sympy-1.0..HEAD


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
