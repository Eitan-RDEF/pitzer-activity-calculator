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


def test_warns_for_extended_but_supported_ph_range() -> None:
    report = validate_solution(SolutionInput(ph=15.0, temperature_c=25.0))

    assert len(report.warnings) == 1
    assert "conventional 0–14 range" in report.warnings[0]


def test_rejects_outside_temperature_range() -> None:
    with pytest.raises(InputValidationError, match="0–100 °C"):
        validate_solution(SolutionInput(ph=7.0, temperature_c=120.0))


def test_rejects_outside_ph_range() -> None:
    with pytest.raises(InputValidationError, match="−2 to 16"):
        validate_solution(SolutionInput(ph=17.0, temperature_c=25.0))


def test_rejects_variable_pressure() -> None:
    with pytest.raises(InputValidationError, match="fixed version 1 pressure"):
        validate_solution(SolutionInput(ph=7.0, temperature_c=25.0, pressure_atm=2.0))


def test_warns_for_conditional_carbonate_divalent_system() -> None:
    report = validate_solution(
        SolutionInput(
            ph=8.0,
            temperature_c=25.0,
            components_molal={"Ca": 0.01, "C4": 0.01},
        )
    )

    assert len(report.warnings) == 1
    assert "incomplete explicit binary Pitzer coverage" in report.warnings[0]


def test_conditional_iron_is_not_exposed_in_core_workflow() -> None:
    with pytest.raises(InputValidationError, match="Fe2"):
        validate_solution(
            SolutionInput(
                ph=7.0,
                temperature_c=25.0,
                components_molal={"Fe2": 0.001, "Cl": 0.002},
            )
        )
