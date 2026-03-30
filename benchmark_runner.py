"""Minimal benchmark runner for comparing two refs using ASV.

This script runs benchmarks for a base and target ref independently and writes
structured JSON results for downstream analysis.

Requires ASV and Git to be installed and configured.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict


def run_asv(
    ref: str,
    config: str,
    results_dir: Path,
    machine: str = "benchmark-runner",
    bench: str = ".*",
) -> None:
    """Run ASV once for a single ref."""
    cmd = [
        "asv",
        "run",
        "--quick",
        "--config",
        config,
        "--results-dir",
        str(results_dir),
        "--machine",
        machine,
        "--bench",
        bench,
        f"{ref}^!",
    ]
    subprocess.run(cmd, check=True)


def load_results(results_dir: Path, commit_hash: str) -> Dict[str, float]:
    """Load benchmark results for a commit from ASV JSON files."""
    result_files = list(results_dir.glob(f"**/{commit_hash[:8]}-*.json")) + list(
        results_dir.glob(f"**/{commit_hash}-*.json")
    ) 

    merged: Dict[str, float] = {}
    for result_file in result_files:
        data = json.loads(result_file.read_text())
        for benchmark_name, payload in data.get("results", {}).items():
            value = extract_numeric(payload.get("result") if isinstance(payload, dict) else payload) 
            if value is not None:
                merged[benchmark_name] = value
    return merged


def extract_numeric(value) -> float | None:
    """Extract the first numeric value from ASV payloads."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, list):
        return next((float(v) for v in value if isinstance(v, (int, float))), None) 
    return None


def rev_parse(ref: str) -> str:
    """Resolve a git ref to a commit hash."""
    return subprocess.run(
        ["git", "rev-parse", ref], check=True, capture_output=True, text=True
    ).stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", default="origin/master")
    parser.add_argument("--target-ref", default="HEAD")
    parser.add_argument("--config", default="asv.conf.json")
    parser.add_argument("--output", default="benchmark_results/runner_report.json")
    parser.add_argument("--machine", default="benchmark-runner")
    parser.add_argument("--bench", default=".*")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    base_hash = rev_parse(args.base_ref)
    target_hash = rev_parse(args.target_ref)

    base_results_dir = output_path.parent / "base_results"
    target_results_dir = output_path.parent / "target_results"
    if base_results_dir.exists():
        shutil.rmtree(base_results_dir)
    if target_results_dir.exists():
        shutil.rmtree(target_results_dir)

    run_asv(args.base_ref, args.config, base_results_dir, machine=args.machine, bench=args.bench)
    run_asv(args.target_ref, args.config, target_results_dir, machine=args.machine, bench=args.bench) 

    report = {
        "metadata": {
            "base_ref": args.base_ref,
            "target_ref": args.target_ref,
            "bench": args.bench,
            "machine": args.machine,
        },
        "base": {
            "ref": args.base_ref,
            "commit": base_hash,
            "results": load_results(base_results_dir, base_hash),
        },
        "target": {
            "ref": args.target_ref,
            "commit": target_hash,
            "results": load_results(target_results_dir, target_hash), 
        },
    }

    output_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()