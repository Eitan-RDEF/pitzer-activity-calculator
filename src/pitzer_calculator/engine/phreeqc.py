"""Narrow adapter around the third-party IPHREEQC Python binding."""

import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pitzer_calculator.config import DEFAULT_DATABASE_PATH
from pitzer_calculator.domain.models import (
    CalculationResult,
    MeanActivityCoefficient,
    SolutionInput,
    SpeciesResult,
)
from pitzer_calculator.domain.species import AQUEOUS_SPECIES, MEAN_ELECTROLYTES
from pitzer_calculator.engine.input_builder import (
    build_phreeqc_input,
    mean_gamma_column,
    species_column,
)
from pitzer_calculator.engine.validation import validate_solution


class CalculationError(RuntimeError):
    """Raised when PHREEQC cannot complete or return the expected output."""


ACTIVE_SPECIES_FLOOR = 1e-90


def _first_float(output: Mapping[str, Any], column: str) -> float:
    try:
        values = output[column]
        return float(values[0])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise CalculationError(f"PHREEQC did not return the expected '{column}' value.") from exc


def _extract_species(output: Mapping[str, Any]) -> tuple[SpeciesResult, ...]:
    results: list[SpeciesResult] = []
    for index, definition in enumerate(AQUEOUS_SPECIES):
        molality = _first_float(output, species_column(index, "m"))
        # PHREEQC uses 1e-99 as a sentinel molality for defined but absent species.
        if molality <= ACTIVE_SPECIES_FLOOR:
            continue
        results.append(
            SpeciesResult(
                name=definition.name,
                charge=definition.charge,
                molality=molality,
                activity=_first_float(output, species_column(index, "a")),
                activity_coefficient=_first_float(output, species_column(index, "gamma")),
                log10_molality=_first_float(output, species_column(index, "lm")),
                log10_activity=_first_float(output, species_column(index, "la")),
                log10_activity_coefficient=_first_float(output, species_column(index, "lg")),
            )
        )
    return tuple(results)


def _extract_mean_coefficients(
    output: Mapping[str, Any], species: tuple[SpeciesResult, ...]
) -> tuple[MeanActivityCoefficient, ...]:
    active = {item.name for item in species if item.molality > ACTIVE_SPECIES_FLOOR}
    return tuple(
        MeanActivityCoefficient(
            key=definition.key,
            label=definition.label,
            value=_first_float(output, mean_gamma_column(definition.key)),
        )
        for definition in MEAN_ELECTROLYTES
        if definition.cation in active and definition.anion in active
    )


def calculate_solution(
    solution: SolutionInput,
    database_path: Path = DEFAULT_DATABASE_PATH,
) -> CalculationResult:
    """Run the complete known-pH, closed-system Pitzer calculation."""

    validate_solution(solution)
    if not database_path.is_file():
        raise CalculationError(f"PHREEQC database not found: {database_path}")

    input_text = build_phreeqc_input(solution)

    try:
        from phreeqc import Phreeqc

        phreeqc = Phreeqc()
        load_status = phreeqc.LoadDatabase(str(database_path))
        if load_status != 0:
            raise CalculationError(
                f"PHREEQC could not load the database: {phreeqc.GetErrorString()}"
            )
        run_status = phreeqc.RunString(input_text)
        if run_status != 0:
            raise CalculationError(f"PHREEQC rejected the calculation: {phreeqc.GetErrorString()}")
        output = phreeqc.GetSelectedOutput()
        engine_version = phreeqc.GetVersionString()
    except ImportError as exc:
        raise CalculationError(
            "The 'phreeqc' package is unavailable. Install the project dependencies first."
        ) from exc
    except CalculationError:
        raise
    except Exception as exc:
        raise CalculationError(f"PHREEQC calculation failed: {exc}") from exc

    if not isinstance(output, Mapping):
        raise CalculationError("PHREEQC returned an unsupported output format.")

    species = _extract_species(output)
    if not species:
        raise CalculationError("PHREEQC returned no active aqueous species.")

    return CalculationResult(
        ph=_first_float(output, "pH"),
        temperature_c=_first_float(output, "temp(C)"),
        pressure_atm=_first_float(output, "pressure_atm"),
        ionic_strength_molal=_first_float(output, "mu"),
        alkalinity_eq_per_kgw=_first_float(output, "Alk(eq/kgw)"),
        water_mass_kg=_first_float(output, "mass_H2O"),
        water_activity=_first_float(output, "water_activity"),
        osmotic_coefficient=_first_float(output, "osmotic_coefficient"),
        charge_balance_eq=_first_float(output, "charge(eq)"),
        charge_balance_error_percent=_first_float(output, "pct_err"),
        species=species,
        mean_activity_coefficients=_extract_mean_coefficients(output, species),
        engine_version=str(engine_version),
        database_sha256=hashlib.sha256(database_path.read_bytes()).hexdigest(),
        phreeqc_input=input_text,
    )


def calculate_h_activity(
    solution: SolutionInput,
    database_path: Path = DEFAULT_DATABASE_PATH,
) -> CalculationResult:
    """Backward-compatible name for callers of the original vertical slice."""

    return calculate_solution(solution, database_path)
