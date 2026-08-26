import pytest

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.engine.validation import InputValidationError, validate_solution


def test_accepts_supported_nonnegative_components() -> None:
    report = validate_solution(
        SolutionInput(ph=7.0, temperature_c=25.0, components_molal={"Na": 0.1, "Cl": 0.1})
    )

    assert report.warnings == ()


def test_rejects_negative_concentration() -> None:
    with pytest.raises(InputValidationError, match="cannot be negative"):
        validate_solution(
            SolutionInput(ph=7.0, temperature_c=25.0, components_molal={"Na": -0.1})
        )


def test_rejects_unknown_component() -> None:
    with pytest.raises(InputValidationError, match="Unsupported components"):
        validate_solution(
            SolutionInput(ph=7.0, temperature_c=25.0, components_molal={"Unknown": 0.1})
        )


def test_warns_outside_initial_validation_envelope() -> None:
    report = validate_solution(SolutionInput(ph=15.0, temperature_c=120.0))

    assert len(report.warnings) == 2

