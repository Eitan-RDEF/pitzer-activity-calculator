"""Validation rules that do not depend on Streamlit or PHREEQC."""

import math
from dataclasses import dataclass

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.domain.species import COMPONENT_BY_KEY


class InputValidationError(ValueError):
    """Raised when a solution cannot be submitted safely."""


@dataclass(frozen=True, slots=True)
class ValidationReport:
    warnings: tuple[str, ...] = ()


def validate_solution(solution: SolutionInput) -> ValidationReport:
    """Validate numeric safety and return non-blocking scientific warnings."""

    if not math.isfinite(solution.ph):
        raise InputValidationError("pH must be a finite number.")
    if not math.isfinite(solution.temperature_c):
        raise InputValidationError("Temperature must be a finite number.")
    if solution.temperature_c <= -273.15:
        raise InputValidationError("Temperature must be above absolute zero.")

    unknown = sorted(set(solution.components_molal) - set(COMPONENT_BY_KEY))
    if unknown:
        raise InputValidationError(f"Unsupported components: {', '.join(unknown)}")

    for key, value in solution.components_molal.items():
        if not math.isfinite(value):
            raise InputValidationError(f"{key} concentration must be finite.")
        if value < 0:
            raise InputValidationError(f"{key} concentration cannot be negative.")

    warnings: list[str] = []
    if not 0 <= solution.temperature_c <= 100:
        warnings.append(
            "The selected temperature is outside the initial 0–100 °C validation range."
        )
    if not 0 <= solution.ph <= 14:
        warnings.append("The selected pH is outside the conventional 0–14 range.")

    return ValidationReport(tuple(warnings))

