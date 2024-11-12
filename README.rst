SymPy's Benchmark Suite
-----------------------

|airspeedvelocity| |image1|

This is the benchmark suite for
`SymPy <http://github.com/sympy/sympy>`__.

These benchmarks track the performance of various features in SymPy
*over time*.

Results are currently hosted in an ad hoc manner, you may find some
results `here <http://hera.physchem.kth.se/~sympy_asv>`__ and
`here <http://www.moorepants.info/misc/sympy-asv/>`__.

The benchmarks are run using `airspeed
velocity <https://asv.readthedocs.io/>`__.

When adding benchmarks, mirror the SymPy directory tree for the feature
you are adding. If your benchmark is not for a specific feature such
that creating subdirectories for your benchmark is not reasonable, put
your benchmark in the top level benchmarking directory.

Quickstart
~~~~~~~~~~

--------------

Installation
^^^^^^^^^^^^

These benchmarks are run using *airspeed velocity* so, you need to have
``asv`` installed,

::

    $ pip install asv

or in conda environment, use

::

    $ conda install -c conda-forge asv

If you're not using conda, you also needs to have ``virtualenv``
installed.

::

    $ pip install virtualenv

Running the benchmarks
^^^^^^^^^^^^^^^^^^^^^^

To quickly try out the benchmarks (e.g. while developing a new benchmark
you can run it against a single commit on sympy master:

::

    $ asv --quick "HEAD^!"

If you work with ``conda`` , you should change the
``"environment_type"`` entry in ``asv.conf.json`` from ``"virtualenv"``
to ``"conda"``. Or you can use,

::

    $ asv --config asv.conf.conda.json --quick "HEAD^!"

You can also run a specific benchmark based on the function or class
name in ``benchmarks/`` or ``slow_benchmarks/`` folder.

::

    $ asv run --bench <Name>

It also supports regular expressions.

The benchmark results will be stored in your ``results/`` folder.

See `asv
documentation <https://asv.readthedocs.io/en/stable/commands.html#asv-run>`__
for additional information.

Running the benchmarks locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently, this suite is pointing to SymPy's base repository for
benchmarking. In order to run these benchmarks on your local checkout,
you will need to change the value of the ``"repo"`` entry in
``asv.conf.json`` and ``asv.conf.conda.json`` files, from the base
repository's url to your local directory where your fork is stored.

This value should be a path, relative to the location of
``asv.conf.json`` config file.

E.g., if your ``sympy`` fork and ``sympy_benchmarks`` are stored in the
same folder then you should change the value of *"repo"* as

::

        "repo" : "../sympy/",

You can also run benchmarks on your remote fork by using the remote
fork's url address instead.

Comparing benchmarks between two branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also compare the benchmarks between two branches/commits. For
that you need to create benchmarks for each one first. Do this for both,

::

    $ asv run -s 1 COMMIT

Then you need to run ``asv compare`` on them.

::

    $ asv compare COMMIT1 COMMIT2

here ``commit`` can be replaced with branch names or commit hashes.

If you are comparing the benchmarks of a branch against master, use the
commit hash of the master that branch is based on. Otherwise, new
unrelated commits in the master can affect the results. Alternately you
can also merge master into the branch first to make sure it is
up-to-date.

Running benchmarks for a selection of commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally we're not interested in benchmarking every single commit to
the sympy repo. For example, we might be interested in some tagged
releases:

::

       $ for release in 1.0 1.1 1.2 1.3 1.4; do asv run "sympy-$release^!"; done

or all the merge commits to the master branch since some tag:

::

       $ git rev-list --merges sympy-1.0..HEAD

Creating and viewing the HTML report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``asv publish`` command to create an HTML report.

It will generate an HTML report in your ``html/`` folder. However, you
may not be able to use the HTML files directly.

After generating the HTML files, you have to use ``asv preview`` to
create a server locally. And navigate to ``http://127.0.0.1:8080/`` to
view the report.

See `asv
documentation <https://asv.readthedocs.io/en/stable/commands.html#asv-publish>`__
for additional information.

.. |airspeedvelocity| image:: http://img.shields.io/badge/benchmarked%20by-asv-green.svg?style=flat
   :target: http://hera.physchem.kth.se/~sympy_asv
.. |image1| image:: https://travis-ci.org/sympy/sympy_benchmarks.png?branch=master
   :target: http://hera.physchem.kth.se/~sympy_asv
