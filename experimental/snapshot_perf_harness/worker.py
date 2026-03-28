from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import statistics
import sys
import time
import traceback
from typing import Any

from sympy import __version__ as sympy_version
from sympy.core.cache import clear_cache

from cases import get_case, list_case_ids, preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one benchmark sample.")
    parser.add_argument("--case", required=True, choices=list_case_ids())
    parser.add_argument("--param", required=True, type=int)
    parser.add_argument("--mode", required=True, choices=("cold", "warm"))
    parser.add_argument("--warmup", type=int)
    parser.add_argument("--repeat", type=int)
    return parser.parse_args()


def measure_once(case: Any, param: int, clear_sympy_cache: bool) -> tuple[int, Any]:
    gc.collect()
    if clear_sympy_cache:
        clear_cache()
    start_ns = time.perf_counter_ns()
    result = case.run(param)
    end_ns = time.perf_counter_ns()
    return end_ns - start_ns, result


def run_sample(args: argparse.Namespace) -> dict[str, Any]:
    case = get_case(args.case)
    warmup_rounds = case.warmup_rounds if args.warmup is None else max(args.warmup, 0)
    repeat_rounds = case.repeat_rounds if args.repeat is None else max(args.repeat, 1)

    if args.mode == "cold":
        duration_ns, result = measure_once(case, args.param, clear_sympy_cache=True)
        inner_durations_ns = [duration_ns]
        sample_duration_ns = duration_ns
    else:
        for _ in range(warmup_rounds):
            case.run(args.param)

        inner_durations_ns = []
        result = None
        for _ in range(repeat_rounds):
            duration_ns, result = measure_once(
                case, args.param, clear_sympy_cache=False
            )
            inner_durations_ns.append(duration_ns)
        sample_duration_ns = int(statistics.median(inner_durations_ns))

    return {
        "case_id": case.case_id,
        "case_label": case.label,
        "param": args.param,
        "mode": args.mode,
        "pid": os.getpid(),
        "python_version": platform.python_version(),
        "sympy_version": sympy_version,
        "platform": platform.platform(),
        "warmup_rounds": warmup_rounds if args.mode == "warm" else 0,
        "repeat_rounds": repeat_rounds if args.mode == "warm" else 1,
        "sample_duration_ns": sample_duration_ns,
        "inner_durations_ns": inner_durations_ns,
        "result_type": type(result).__name__,
        "result_preview": preview(result),
    }


def main() -> int:
    args = parse_args()
    try:
        payload = run_sample(args)
    except Exception as exc:  # noqa: BLE001
        error_payload = {
            "case_id": args.case,
            "param": args.param,
            "mode": args.mode,
            "pid": os.getpid(),
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        print(json.dumps(error_payload))
        return 1

    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
