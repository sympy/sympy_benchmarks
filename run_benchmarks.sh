#!/bin/bash
# some useful options:
#   --show-stderr
if which conda; then
    echo "Using conda"
    asv run --config asv.conf.conda.json $@
else
    echo "Using virtualenv"
    asv run --config asv.conf.venv.json $@
fi
