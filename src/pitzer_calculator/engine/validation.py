"""Validation rules that do not depend on Streamlit or PHREEQC."""

import math
from dataclasses import dataclass

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.domain.species import COMPONENT_BY_KEY, CONDITIONAL_COMPONENTS


class InputValidationError(ValueError):
    """Raised when a solution cannot be submitted safely."""


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Non-blocking scientific warnings produced after an input passes validation."""

    warnings: tuple[str, ...] = ()


def validate_solution(solution: SolutionInput) -> ValidationReport:
    """Validate numeric safety and return non-blocking scientific warnings."""

    if not math.isfinite(solution.ph):
        raise InputValidationError("pH must be a finite number.")
    if not math.isfinite(solution.temperature_c):
        raise InputValidationError("Temperature must be a finite number.")
    if not 0 <= solution.temperature_c <= 100:
        raise InputValidationError("Temperature must be within the version 1 range of 0–100 °C.")
    if not math.isfinite(solution.pressure_atm) or solution.pressure_atm != 1.0:
        raise InputValidationError("This workflow requires the fixed version 1 pressure of 1 atm.")
    if not -2 <= solution.ph <= 16:
        raise InputValidationError("pH must be within the version 1 range of −2 to 16.")

    unknown = sorted(set(solution.components_molal) - set(COMPONENT_BY_KEY))
    if unknown:
        raise InputValidationError(f"Unsupported components: {', '.join(unknown)}")

    for key, value in solution.components_molal.items():
        if not math.isfinite(value):
            raise InputValidationError(f"{key} concentration must be finite.")
        if value < 0:
            raise InputValidationError(f"{key} concentration cannot be negative.")

    warnings: list[str] = []
    active = {
        key for key, concentration in solution.components_molal.items() if concentration > 0
    }
    if not 0 <= solution.ph <= 14:
        warnings.append("The selected pH is outside the conventional 0–14 range.")

    for component in CONDITIONAL_COMPONENTS:
        if component.key in active and component.limitation:
            warnings.append(
                f"{component.label} has conditional database coverage: "
                f"{component.limitation} Independently validate this result."
            )

    if solution.components_molal.get("C4", 0.0) > 0 and (
        solution.components_molal.get("Ca", 0.0) > 0
        or solution.components_molal.get("Mg", 0.0) > 0
    ):
        warnings.append(
            "Carbonate with Ca or Mg has incomplete explicit binary Pitzer coverage in the "
            "bundled database. Treat this result as conditional and independently validate it."
        )

    if "Br" in active and len(active) > 2:
        warnings.append(
            "This multicomponent bromide mixture has less complete ternary interaction "
            "coverage than a binary bromide salt."
        )

    if "Li" in active and ("C4" in active or "SO4" in active):
        warnings.append(
            "Li is combined with C(IV) or S(VI), activating known gaps for carbonate, "
            "bicarbonate, or bisulfate interactions."
        )

    if "Sr" in active and "C4" in active:
        warnings.append(
            "Sr with C(IV) activates incomplete carbonate and bicarbonate interaction coverage."
        )
    if "Sr" in active and solution.ph >= 9:
        warnings.append(
            "Sr at pH 9 or above may be affected by missing explicit hydroxide interactions."
        )
    if "Sr" in active and "SO4" in active and solution.ph <= 4:
        warnings.append(
            "Sr with S(VI) at low pH may be affected by missing bisulfate interactions."
        )

    if "Ba" in active and ("SO4" in active or "C4" in active):
        warnings.append(
            "Ba with sulfate or carbonate can be strongly affected by mineral precipitation, "
            "but this aqueous-only calculation does not equilibrate solids."
        )

    if "Si" in active and solution.ph >= 9:
        warnings.append(
            "At pH 9 or above, deprotonated silicate species become increasingly relevant and "
            "have sparse explicit Pitzer interaction coverage in this database."
        )

    return ValidationReport(tuple(warnings))
