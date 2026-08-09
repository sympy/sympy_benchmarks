from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from sympy import Poly, Symbol, exp, log, series, sin


CaseRunner = Callable[[int], Any]


@dataclass(frozen=True)
class CaseDef:
    case_id: str
    label: str
    default_params: tuple[int, ...]
    run: CaseRunner
    warmup_rounds: int = 2
    repeat_rounds: int = 3


def preview(result: Any, limit: int = 160) -> str:
    text = " ".join(str(result).split())
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3]}..."


def run_poly_mul(param: int) -> Any:
    x = Symbol("x")
    left = Poly((x + 1) ** param, x)
    right = Poly((x - 1) ** param, x)
    return left * right


def run_composed_series(param: int) -> Any:
    x = Symbol("x")
    expr = exp(sin(x)) * log(1 + x)
    return series(expr, x, 0, param)


CASE_REGISTRY = {
    "poly_mul": CaseDef(
        case_id="poly_mul",
        label="Multiply two Poly objects built from (x +/- 1)**N.",
        default_params=(10, 20, 30),
        run=run_poly_mul,
    ),
    "composed_series": CaseDef(
        case_id="composed_series",
        label="Expand exp(sin(x)) * log(1 + x) as a power series.",
        default_params=(6, 8, 10),
        run=run_composed_series,
    ),
}


def get_case(case_id: str) -> CaseDef:
    try:
        return CASE_REGISTRY[case_id]
    except KeyError as exc:
        known = ", ".join(sorted(CASE_REGISTRY))
        raise KeyError(f"Unknown case '{case_id}'. Known cases: {known}") from exc


def list_case_ids() -> list[str]:
    return sorted(CASE_REGISTRY)
