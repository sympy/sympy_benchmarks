#!/bin/bash -eu
if [[ "$TRAVIS" == "true" ]]; then echo -en "travis_fold:start:test-${tag}\\r"; fi
tag=$1
python3 -m virtualenv /tmp/venv-${tag}
echo "Running the benchmark test suite for ${tag}..."
bash -c "source /tmp/venv-${tag}/bin/activate; pip install pytest ${tag//-/==} && pytest -rs"
echo "Running benchmarks for ${tag}..."
asv run --machine travis_dummy_machine --config asv.conf.venv.json --show-stderr "${tag}^!"
if [[ "$TRAVIS" == "true" ]]; then echo -en "travis_fold:end:test-${tag}\\r"; fi
