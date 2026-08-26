"""Narrow adapter around the third-party IPHREEQC Python binding."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pitzer_calculator.config import DEFAULT_DATABASE_PATH
from pitzer_calculator.domain.models import CalculationResult, SolutionInput
from pitzer_calculator.engine.input_builder import build_phreeqc_input
from pitzer_calculator.engine.validation import validate_solution


class CalculationError(RuntimeError):
    """Raised when PHREEQC cannot complete or return the expected output."""


def _first_float(output: Mapping[str, Any], column: str) -> float:
    try:
        values = output[column]
        return float(values[0])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise CalculationError(f"PHREEQC did not return the expected '{column}' value.") from exc


def calculate_h_activity(
    solution: SolutionInput,
    database_path: Path = DEFAULT_DATABASE_PATH,
) -> CalculationResult:
    """Run the initial H+ activity calculation using the bundled Pitzer database."""

    validate_solution(solution)
    if not database_path.is_file():
        raise CalculationError(f"PHREEQC database not found: {database_path}")

    input_text = build_phreeqc_input(solution)

    try:
        from phreeqc import Phreeqc

        phreeqc = Phreeqc()
        phreeqc.LoadDatabase(str(database_path))
        phreeqc.RunString(input_text)
        output = phreeqc.GetSelectedOutput()
    except ImportError as exc:
        raise CalculationError(
            "The 'phreeqc' package is unavailable. Install the project dependencies first."
        ) from exc
    except Exception as exc:
        raise CalculationError(f"PHREEQC calculation failed: {exc}") from exc

    if not isinstance(output, Mapping):
        raise CalculationError("PHREEQC returned an unsupported output format.")

    return CalculationResult(
        ph=_first_float(output, "pH"),
        ionic_strength_molal=_first_float(output, "mu"),
        charge_balance_error_percent=_first_float(output, "pct_err"),
        log10_h_activity=_first_float(output, "loga_H"),
        log10_h_molality=_first_float(output, "logm_H"),
        log10_h_activity_coefficient=_first_float(output, "loggamma_H"),
        h_activity_coefficient=_first_float(output, "gamma_H"),
        h_molality=_first_float(output, "mol_H"),
        h_activity=_first_float(output, "act_H"),
        phreeqc_input=input_text,
    )
