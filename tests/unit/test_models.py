import pytest

from pitzer_calculator.domain.models import (
    CalculationResult,
    ConcentrationUnit,
    convert_composition_to_molal,
)


def test_converts_millimolal_composition_to_molal() -> None:
    converted = convert_composition_to_molal(
        {"Na": 100.0, "Cl": 100.0}, ConcentrationUnit.MMOL_PER_KGW
    )

    assert converted == pytest.approx({"Na": 0.1, "Cl": 0.1})


@pytest.mark.parametrize(
    ("error", "expected"),
    [(2.0, "good"), (-2.01, "review"), (5.0, "review"), (5.01, "significant")],
)
def test_charge_balance_classification(error: float, expected: str) -> None:
    result = CalculationResult(
        ph=7.0,
        temperature_c=25.0,
        pressure_atm=1.0,
        ionic_strength_molal=0.1,
        alkalinity_eq_per_kgw=0.0,
        water_mass_kg=1.0,
        water_activity=0.99,
        osmotic_coefficient=0.95,
        charge_balance_eq=0.0,
        charge_balance_error_percent=error,
        species=(),
        mean_activity_coefficients=(),
        engine_version="test",
        database_sha256="0" * 64,
        phreeqc_input="END\n",
    )

    assert result.charge_balance_status == expected

