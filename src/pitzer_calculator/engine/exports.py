"""Deterministic, stateless calculation exports."""

import csv
import io
import zipfile
from collections.abc import Iterable

from pitzer_calculator.domain.models import CalculationResult, SolutionInput
from pitzer_calculator.domain.species import COMPONENT_BY_KEY, COMPONENTS


def _number(value: float) -> str:
    return format(value, ".15g")


def species_csv(result: CalculationResult) -> str:
    """Return the complete active-species table as UTF-8-compatible CSV text."""

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "species",
            "charge",
            "molality_mol_per_kg_water",
            "activity",
            "activity_coefficient",
            "log10_molality",
            "log10_activity",
            "log10_activity_coefficient",
        ]
    )
    for species in result.species:
        writer.writerow(
            [
                species.name,
                species.charge,
                _number(species.molality),
                _number(species.activity),
                _number(species.activity_coefficient),
                _number(species.log10_molality),
                _number(species.log10_activity),
                _number(species.log10_activity_coefficient),
            ]
        )
    return buffer.getvalue()


def calculation_report(
    solution: SolutionInput,
    result: CalculationResult,
    warnings: Iterable[str] = (),
) -> str:
    """Return a concise human-readable Markdown calculation record."""

    warning_list = tuple(warnings)
    fixed_redox_components = [
        COMPONENT_BY_KEY[key].label
        for key in ("Fe2", "Mn2")
        if solution.components_molal.get(key, 0.0) > 0
    ]
    if fixed_redox_components:
        redox_statement = (
            "- Redox calculation: disabled; "
            f"{', '.join(fixed_redox_components)} remain fixed in the +II oxidation state"
        )
    else:
        redox_statement = "- Redox calculation: disabled; no redox-sensitive inputs are active"
    lines = [
        "# Pitzer Activity Calculation Report",
        "",
        (
            "> Selected outputs have been compared with published USGS and NIST reference "
            "data. Validation does not cover every composition, output, or operating "
            "condition. Independently verify results used for critical engineering decisions."
        ),
        "",
        "## Inputs",
        "",
        "- Mode: known pH, closed aqueous system",
        f"- pH: {_number(solution.ph)} (hydrogen-ion activity basis)",
        f"- Temperature: {_number(solution.temperature_c)} °C",
        f"- Pressure: {_number(solution.pressure_atm)} atm",
        "- Internal concentration basis: mol/kg H2O",
        "",
        "| Analytical component | Molality (mol/kg H2O) |",
        "|---|---:|",
    ]
    for component in COMPONENTS:
        value = solution.components_molal.get(component.key, 0.0)
        if value > 0:
            lines.append(f"| {component.label} | {_number(value)} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Ionic strength: {_number(result.ionic_strength_molal)} mol/kg H2O",
            f"- Water activity: {_number(result.water_activity)}",
            f"- Osmotic coefficient: {_number(result.osmotic_coefficient)}",
            f"- Alkalinity: {_number(result.alkalinity_eq_per_kgw)} eq/kg H2O",
            f"- Charge-balance error: {_number(result.charge_balance_error_percent)}%",
            f"- Charge-balance classification: {result.charge_balance_status}",
            "",
            "## Warnings",
            "",
        ]
    )
    if warning_list:
        lines.extend(f"- {warning}" for warning in warning_list)
    else:
        lines.append("- No input-specific warnings were generated.")

    lines.extend(
        [
            "",
            "## Mean activity coefficients",
            "",
            "| Electrolyte | gamma +/- |",
            "|---|---:|",
        ]
    )
    if result.mean_activity_coefficients:
        lines.extend(
            f"| {item.label} | {_number(item.value)} |"
            for item in result.mean_activity_coefficients
        )
    else:
        lines.append("| None available for the active ion pairs | — |")

    lines.extend(
        [
            "",
            "## Active aqueous species",
            "",
            "| Species | Charge | Molality | Activity | Activity coefficient |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    lines.extend(
        "| "
        f"{item.name} | {item.charge} | {_number(item.molality)} | "
        f"{_number(item.activity)} | {_number(item.activity_coefficient)} |"
        for item in result.species
    )

    lines.extend(
        [
            "",
            "## Scientific and reproducibility metadata",
            "",
            "- Activity model: Pitzer",
            "- Individual-ion convention: MacInnes scaling",
            "- Electrostatic mixing terms: enabled",
            redox_statement,
            "- Mineral precipitation/equilibration: not modeled",
            f"- PHREEQC engine: {result.engine_version}",
            f"- Database SHA-256: `{result.database_sha256}`",
            "",
            "The accompanying `.pqi` file is the exact PHREEQC input used for this result.",
            "",
        ]
    )
    return "\n".join(lines)


def calculation_bundle(
    solution: SolutionInput,
    result: CalculationResult,
    warnings: Iterable[str] = (),
) -> bytes:
    """Return a ZIP containing the input, species CSV, and human report."""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("pitzer-calculation.pqi", result.phreeqc_input)
        archive.writestr("pitzer-species.csv", species_csv(result))
        archive.writestr("pitzer-report.md", calculation_report(solution, result, warnings))
    return buffer.getvalue()


def input_component_label(key: str) -> str:
    """Return the public analytical-component label for export extensions."""

    return COMPONENT_BY_KEY[key].label
