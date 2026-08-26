import os

import pytest

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.engine.phreeqc import calculate_solution

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the native PHREEQC smoke test.",
)


def test_calculates_balanced_nacl_solution() -> None:
    result = calculate_solution(
        SolutionInput(
            ph=7.0,
            temperature_c=25.0,
            components_molal={"Na": 0.1, "Cl": 0.1},
        )
    )

    assert result.ionic_strength_molal > 0
    assert result.h_activity_coefficient > 0
    assert {item.name for item in result.species} == {"H+", "OH-", "Na+", "Cl-"}
    assert [item.key for item in result.mean_activity_coefficients] == ["NaCl"]
    assert result.engine_version in {"3.8.6-17100", "3.8.6-17100-x64"}
    assert result.pressure_atm == pytest.approx(1.0)


def test_database_exposes_mean_gamma_and_water_properties() -> None:
    """Pin the complete engine result for 1 molal NaCl at 25 °C."""
    result = calculate_solution(
        SolutionInput(
            ph=7.0,
            temperature_c=25.0,
            components_molal={"Na": 1.0, "Cl": 1.0},
        )
    )

    assert result.mean_activity_coefficients[0].value == pytest.approx(0.657220, rel=1e-5)
    assert result.water_activity == pytest.approx(0.966825, rel=1e-5)
    assert result.osmotic_coefficient == pytest.approx(0.936359, rel=1e-5)
    sodium = result.species_by_name("Na+")
    assert sodium.activity == pytest.approx(
        sodium.molality * sodium.activity_coefficient, rel=1e-12
    )


def test_extracts_complete_core_mixed_solution_species() -> None:
    result = calculate_solution(
        SolutionInput(
            ph=8.1,
            temperature_c=60.0,
            components_molal={
                "Na": 0.6,
                "K": 0.02,
                "Mg": 0.05,
                "Ca": 0.01,
                "Cl": 0.6,
                "SO4": 0.04,
                "C4": 0.002,
            },
        )
    )

    assert {item.name for item in result.species} == {
        "H+",
        "OH-",
        "Na+",
        "K+",
        "Mg+2",
        "Ca+2",
        "Cl-",
        "SO4-2",
        "HSO4-",
        "CO3-2",
        "HCO3-",
        "CO2",
        "MgOH+",
        "MgCO3",
    }
    assert {item.key for item in result.mean_activity_coefficients} == {
        "NaCl",
        "KCl",
        "CaCl2",
        "MgCl2",
        "Na2SO4",
    }
    assert result.charge_balance_status == "review"


def test_extracts_conditional_components_and_their_aqueous_species() -> None:
    result = calculate_solution(
        SolutionInput(
            ph=10.0,
            temperature_c=25.0,
            components_molal={
                "Na": 0.1,
                "Cl": 0.1,
                "Br": 0.01,
                "Li": 0.005,
                "Sr": 0.001,
                "Ba": 0.0001,
                "B": 0.002,
                "Si": 0.002,
                "Fe2": 0.0002,
                "Mn2": 0.0002,
            },
        )
    )

    active_species = {item.name for item in result.species}
    assert {
        "Br-",
        "Li+",
        "Sr+2",
        "Ba+2",
        "Fe+2",
        "Mn+2",
        "B(OH)3",
        "B(OH)4-",
        "B3O3(OH)4-",
        "B4O5(OH)4-2",
        "H4SiO4",
        "H3SiO4-",
        "H2SiO4-2",
    } <= active_species
    assert "HBr" in {item.key for item in result.mean_activity_coefficients}
