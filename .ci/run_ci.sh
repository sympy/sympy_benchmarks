#!/bin/bash -eu
tag=$1
if [[ ${TRAVIS:-} ]]; then echo -en "travis_fold:start:test-${tag}\\r"; fi
python3 -m virtualenv /tmp/venv-${tag}
bash -c "source /tmp/venv-${tag}/bin/activate; pip install pytest https://github.com/sympy/sympy/archive/${tag}.tar.gz && echo \"Running the benchmark test suite for ${tag}...\" && pytest -rs"
echo "Running benchmarks for ${tag}..."
asv run --machine travis --config asv.conf.venv.json --show-stderr "${tag}^!"
if [[ ${TRAVIS:-} ]]; then echo -en "travis_fold:end:test-${tag}\\r"; fi
