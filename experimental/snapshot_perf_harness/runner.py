from __future__ import annotations

import argparse
import json
import platform
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cases import get_case, list_case_ids


ROOT = Path(__file__).resolve().parent
WORKER = ROOT / "worker.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the snapshot-style benchmark demo.")
    parser.add_argument(
        "--cases",
        nargs="+",
        default=list_case_ids(),
        choices=list_case_ids(),
        help="Case ids to run.",
    )
    parser.add_argument(
        "--modes",
        nargs="+",
        default=["cold", "warm"],
        choices=("cold", "warm"),
        help="Execution modes to run.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=5,
        help="Independent worker samples per case/param/mode.",
    )
    parser.add_argument(
        "--params",
        nargs="+",
        type=int,
        help="Optional override for all case parameters.",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        help="Optional warmup override for warm samples.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        help="Optional inner repeat override for warm samples.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path for the full benchmark report.",
    )
    return parser.parse_args()


def ns_to_ms(duration_ns: int | float) -> float:
    return float(duration_ns) / 1_000_000.0


def median_absolute_deviation(samples: list[int]) -> float:
    median_value = statistics.median(samples)
    deviations = [abs(sample - median_value) for sample in samples]
    return float(statistics.median(deviations))


def summarize_samples(samples: list[int]) -> dict[str, Any]:
    median_value = int(statistics.median(samples))
    minimum = min(samples)
    maximum = max(samples)
    mean = statistics.fmean(samples)
    mad_ns = median_absolute_deviation(samples)
    summary = {
        "sample_count": len(samples),
        "median_ns": median_value,
        "mean_ns": mean,
        "min_ns": minimum,
        "max_ns": maximum,
        "mad_ns": mad_ns,
        "median_ms": ns_to_ms(median_value),
        "mean_ms": ns_to_ms(mean),
        "min_ms": ns_to_ms(minimum),
        "max_ms": ns_to_ms(maximum),
        "mad_ms": ns_to_ms(mad_ns),
    }
    if len(samples) > 1:
        summary["stdev_ns"] = statistics.stdev(samples)
        summary["stdev_ms"] = ns_to_ms(summary["stdev_ns"])
    else:
        summary["stdev_ns"] = 0.0
        summary["stdev_ms"] = 0.0
    return summary


def run_worker(
    case_id: str,
    param: int,
    mode: str,
    warmup: int | None,
    repeat: int | None,
) -> dict[str, Any]:
    command = [
        sys.executable,
        str(WORKER),
        "--case",
        case_id,
        "--param",
        str(param),
        "--mode",
        mode,
    ]
    if warmup is not None:
        command.extend(["--warmup", str(warmup)])
    if repeat is not None:
        command.extend(["--repeat", str(repeat)])

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = completed.stdout.strip()
    if not stdout:
        raise RuntimeError(
            f"Worker produced no JSON output for case={case_id} param={param} mode={mode}.\n"
            f"stderr:\n{completed.stderr}"
        )

    payload = json.loads(stdout)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Worker failed for case={case_id} param={param} mode={mode}:\n"
            f"{payload.get('traceback', payload.get('error', stdout))}"
        )
    return payload


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host_platform": platform.platform(),
        "host_python": platform.python_version(),
        "execution_model": {
            "cold": "fresh process, one timed call",
            "warm": "fresh process, warmup first, then take the median of repeated timed calls",
        },
        "repeatability_note": (
            "Each case/param/mode is sampled with independent worker processes. "
            "The primary summary statistic is the median."
        ),
        "primary_statistic": "median",
        "samples_per_configuration": args.samples,
        "cases": [],
    }

    for case_id in args.cases:
        case = get_case(case_id)
        params = tuple(args.params) if args.params else case.default_params
        for param in params:
            for mode in args.modes:
                worker_payloads = []
                sample_durations = []
                for _ in range(args.samples):
                    payload = run_worker(
                        case_id=case_id,
                        param=param,
                        mode=mode,
                        warmup=args.warmup,
                        repeat=args.repeat,
                    )
                    worker_payloads.append(payload)
                    sample_durations.append(payload["sample_duration_ns"])

                summary = summarize_samples(sample_durations)
                entry = {
                    "case_id": case_id,
                    "case_label": case.label,
                    "param": param,
                    "mode": mode,
                    "summary": summary,
                    "workers": worker_payloads,
                }
                report["cases"].append(entry)

                print(
                    f"[{mode:4}] {case_id:16} param={param:<4} "
                    f"med={summary['median_ms']:.3f} ms "
                    f"min={summary['min_ms']:.3f} ms "
                    f"max={summary['max_ms']:.3f} ms"
                )

    return report


def main() -> int:
    args = parse_args()
    if args.samples < 1:
        raise SystemExit("--samples must be at least 1")

    report = build_report(args)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nWrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
