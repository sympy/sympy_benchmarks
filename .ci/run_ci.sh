#!/bin/bash
git clone --bare git://github.com/sympy/sympy sympy  # asv uses --bare
for tag in $(cd sympy; git tag --contains sympy-1.0 | grep -v rc) master; do  # loops over releases since 1.0 (and master)
    python3 -m virtualenv /tmp/venv-${tag}
    echo "Running the benchmark test suite for ${tag}..."
    bash -c "source /tmp/venv-${tag}/bin/activate; pip install pytest ${tag} && pytest -rs"
    echo "Running benchmarks for ${tag}..."
    asv run --config asv.conf.venv.json --show-stderr "${tag}^!"
done
