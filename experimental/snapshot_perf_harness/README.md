# Snapshot-Style Performance Harness Demo

This directory is a small proof of concept for the cold-cache benchmarking
workflow described in my SymPy GSoC proposal. It is not meant to be a finished
benchmark framework. It is meant to show that the core execution model already
works in code.

The current prototype demonstrates five things:

- cold samples can be run in fresh worker processes
- warm measurements can be separated from cold measurements
- each configuration can be sampled repeatedly with independent workers
- results can be stored as structured JSON rather than ad hoc terminal output
- a small curated set of workload families can be run without changing the
  runner core

## Files

- `cases.py`: case registry and workload definitions
- `worker.py`: runs one isolated sample and emits JSON
- `runner.py`: orchestrates repeated samples and summarizes them

## What this PoC is proving

The main point of this prototype is to show a measurement model that is closer
to SymPy's cold-cache performance questions than a loop-based benchmark body.

- In `cold` mode, each sample starts in a fresh Python process and times one
  call.
- In `warm` mode, each sample still gets its own worker process, but the worker
  warms up first and then records repeated timed calls.
- For each case/parameter/mode combination, the runner collects multiple
  independent samples and summarizes them.

The report treats the median as the primary statistic. That is deliberate: for
small benchmark runs, median is usually a better headline number than a single
sample or a raw mean.

## Run it

From the repo root:

```bash
python3 experimental/snapshot_perf_harness/runner.py \
  --samples 3 \
  --output experimental/snapshot_perf_harness/results/demo_report.json
```

Run one workload family across several parameter points:

```bash
python3 experimental/snapshot_perf_harness/runner.py \
  --cases poly_mul \
  --params 10 20 30 \
  --modes cold warm
```

Inspect one worker directly:

```bash
python3 experimental/snapshot_perf_harness/worker.py \
  --case poly_mul \
  --param 10 \
  --mode cold
```

## Current scope

This prototype already includes:

- fresh-process cold samples
- one-execution cold timing
- repeated independent sampling
- summary statistics over raw samples
- multiple parameter points, so the same case family can be used for basic
  scaling studies
- machine-readable JSON output with raw worker payloads

This prototype does not yet include:

- scheduled execution on a dedicated benchmark machine
- baseline update or comparison workflows
- plots, dashboards, or website output
- integration with the existing benchmark repo infrastructure
- a larger curated suite of real SymPy workloads

## How I would cite it in the proposal

I would describe this as a proposal companion prototype, not as a completed
framework. The current code is enough to support these claims:

- the parent/worker execution model is already implemented
- cold and warm paths are already separated
- repeatability is handled through repeated independent samples
- stored JSON output is already available for later comparison work

That is the level of evidence I want from a PoC: enough to show that the core
design is real, without pretending that the full project has already been done.
