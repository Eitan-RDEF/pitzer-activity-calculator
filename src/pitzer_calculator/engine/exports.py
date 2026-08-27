"""Deterministic, stateless calculation exports."""

import csv
import io
import zipfile
from collections.abc import Iterable

from pitzer_calculator.domain.models import CalculationResult, SolutionInput
from pitzer_calculator.domain.species import COMPONENT_BY_KEY, COMPONENTS


def _number(value: float) -> str:
    """Format deterministic export precision independently from the UI."""

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


def complete_results_csv(result: CalculationResult) -> str:
    """Return every result view in one rectangular, machine-readable CSV.

    Different result groups expose different properties. A shared set of columns keeps the
    file valid for spreadsheet and data-analysis tools; cells that do not apply to a row are
    intentionally left empty.
    """

    fieldnames = [
        "section",
        "name",
        "value",
        "unit",
        "charge",
        "molality_mol_per_kg_water",
        "activity",
        "activity_coefficient",
        "log10_molality",
        "log10_activity",
        "log10_activity_coefficient",
    ]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()

    summary_rows = (
        ("pH", result.ph, "dimensionless"),
        ("ionic_strength", result.ionic_strength_molal, "mol/kg H2O"),
        ("water_activity", result.water_activity, "dimensionless"),
        ("osmotic_coefficient", result.osmotic_coefficient, "dimensionless"),
    )
    for name, value, unit in summary_rows:
        writer.writerow(
            {"section": "summary", "name": name, "value": _number(value), "unit": unit}
        )

    condition_rows = (
        ("temperature", result.temperature_c, "degC"),
        ("pressure", result.pressure_atm, "atm"),
        ("alkalinity", result.alkalinity_eq_per_kgw, "eq/kg H2O"),
        ("charge_balance", result.charge_balance_eq, "eq"),
        ("charge_balance_error", result.charge_balance_error_percent, "percent"),
    )
    for name, value, unit in condition_rows:
        writer.writerow(
            {
                "section": "conditions_and_balance",
                "name": name,
                "value": _number(value),
                "unit": unit,
            }
        )
    writer.writerow(
        {
            "section": "conditions_and_balance",
            "name": "charge_balance_classification",
            "value": result.charge_balance_status,
        }
    )

    for item in result.mean_activity_coefficients:
        writer.writerow(
            {
                "section": "mean_activity_coefficients",
                "name": item.label,
                "value": _number(item.value),
                "unit": "dimensionless",
            }
        )

    for species in result.species:
        writer.writerow(
            {
                "section": "aqueous_species",
                "name": species.name,
                "charge": species.charge,
                "molality_mol_per_kg_water": _number(species.molality),
                "activity": _number(species.activity),
                "activity_coefficient": _number(species.activity_coefficient),
                "log10_molality": _number(species.log10_molality),
                "log10_activity": _number(species.log10_activity),
                "log10_activity_coefficient": _number(
                    species.log10_activity_coefficient
                ),
            }
        )

    method_rows = (
        ("activity_model", "Pitzer"),
        ("individual_ion_convention", "MacInnes scaling"),
        ("system_boundary", "known pH, closed aqueous system"),
        ("redox_equilibrium", "disabled; Fe and Mn remain fixed as +II"),
        ("phase_equilibration", "disabled for solids and gases"),
        ("charge_correction", "not applied"),
        ("PHREEQC_engine_version", result.engine_version),
        ("database_SHA256", result.database_sha256),
    )
    for name, value in method_rows:
        writer.writerow({"section": "method_and_versions", "name": name, "value": value})

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
