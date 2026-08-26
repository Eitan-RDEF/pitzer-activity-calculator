import io
import zipfile

from pitzer_calculator.domain.models import (
    CalculationResult,
    MeanActivityCoefficient,
    SolutionInput,
    SpeciesResult,
)
from pitzer_calculator.engine.exports import calculation_bundle, calculation_report, species_csv


def _result() -> CalculationResult:
    return CalculationResult(
        ph=7.0,
        temperature_c=25.0,
        pressure_atm=1.0,
        ionic_strength_molal=0.1,
        alkalinity_eq_per_kgw=1e-7,
        water_mass_kg=1.0,
        water_activity=0.996,
        osmotic_coefficient=0.94,
        charge_balance_eq=0.0,
        charge_balance_error_percent=0.0,
        species=(
            SpeciesResult("Na+", 1, 0.1, 0.08, 0.8, -1.0, -1.09691, -0.09691),
        ),
        mean_activity_coefficients=(MeanActivityCoefficient("NaCl", "NaCl", 0.78),),
        engine_version="3.8.6-test",
        database_sha256="a" * 64,
        phreeqc_input="SOLUTION 1\nEND\n",
    )


def test_species_csv_contains_full_precision_columns() -> None:
    csv_text = species_csv(_result())

    assert "molality_mol_per_kg_water" in csv_text
    assert "Na+,1,0.1,0.08,0.8" in csv_text


def test_report_records_assumptions_versions_and_warning() -> None:
    solution = SolutionInput(7.0, 25.0, {"Na": 0.1, "Cl": 0.1})
    report = calculation_report(solution, _result(), ["Example warning"])

    assert "known pH, closed aqueous system" in report
    assert "MacInnes scaling" in report
    assert "PHREEQC engine: 3.8.6-test" in report
    assert "Example warning" in report


def test_bundle_contains_all_reproducibility_files() -> None:
    solution = SolutionInput(7.0, 25.0, {"Na": 0.1, "Cl": 0.1})
    bundle = calculation_bundle(solution, _result())

    with zipfile.ZipFile(io.BytesIO(bundle)) as archive:
        assert set(archive.namelist()) == {
            "pitzer-calculation.pqi",
            "pitzer-report.md",
            "pitzer-species.csv",
        }

