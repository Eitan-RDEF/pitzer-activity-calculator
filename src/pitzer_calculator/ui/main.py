"""Streamlit composition for the complete core calculation workflow."""

from typing import Any

import streamlit as st

from pitzer_calculator.config import APP_NAME, APP_TAGLINE
from pitzer_calculator.domain.models import (
    ConcentrationUnit,
    SolutionInput,
    convert_composition_to_molal,
)
from pitzer_calculator.domain.species import COMPONENTS
from pitzer_calculator.engine.exports import (
    calculation_bundle,
    calculation_report,
    species_csv,
)
from pitzer_calculator.engine.phreeqc import CalculationError, calculate_solution
from pitzer_calculator.engine.validation import InputValidationError, validate_solution
from pitzer_calculator.ui.styles import apply_styles


def _display_number(value: float, significant_digits: int = 6) -> str:
    return format(value, f".{significant_digits}g")


def _composition_inputs(unit: ConcentrationUnit) -> dict[str, float]:
    values: dict[str, float] = {}
    for group in ("Cations", "Anions and totals"):
        with st.expander(group, expanded=True):
            columns = st.columns(3)
            group_components = [item for item in COMPONENTS if item.group == group]
            for index, component in enumerate(group_components):
                with columns[index % len(columns)]:
                    default = component.default_molal / unit.to_molal_factor
                    values[component.key] = st.number_input(
                        f"{component.label} [{unit.display_label}]",
                        min_value=0.0,
                        value=default,
                        format="%.8g",
                        key=f"component_{unit.name}_{component.key}",
                    )
    return values


def _species_rows(result: Any) -> list[dict[str, Any]]:
    return [
        {
            "Species": item.name,
            "Charge": item.charge,
            "Molality [mol/kg H₂O]": item.molality,
            "Activity": item.activity,
            "Activity coefficient γ": item.activity_coefficient,
            "log₁₀ molality": item.log10_molality,
            "log₁₀ activity": item.log10_activity,
            "log₁₀ γ": item.log10_activity_coefficient,
        }
        for item in result.species
    ]


def _render_charge_status(result: Any) -> None:
    value = abs(result.charge_balance_error_percent)
    if result.charge_balance_status == "good":
        st.success(f"Charge balance: good ({value:.3g}% absolute error; target ≤2%).")
    elif result.charge_balance_status == "review":
        st.warning(f"Charge balance: review recommended ({value:.3g}% absolute error).")
    else:
        st.error(f"Charge balance: significant imbalance ({value:.3g}% absolute error).")


def _render_downloads(solution: SolutionInput, result: Any, warnings: tuple[str, ...]) -> None:
    report = calculation_report(solution, result, warnings)
    first, second, third, fourth = st.columns(4)
    first.download_button(
        "Species CSV",
        data=species_csv(result),
        file_name="pitzer-species.csv",
        mime="text/csv",
        width="stretch",
    )
    second.download_button(
        "PHREEQC input",
        data=result.phreeqc_input,
        file_name="pitzer-calculation.pqi",
        mime="text/plain",
        width="stretch",
    )
    third.download_button(
        "Calculation report",
        data=report,
        file_name="pitzer-report.md",
        mime="text/markdown",
        width="stretch",
    )
    fourth.download_button(
        "Complete ZIP",
        data=calculation_bundle(solution, result, warnings),
        file_name="pitzer-calculation.zip",
        mime="application/zip",
        width="stretch",
    )


def _render_results(solution: SolutionInput, result: Any, warnings: tuple[str, ...]) -> None:
    st.subheader("Calculation results")
    _render_charge_status(result)

    first, second, third, fourth = st.columns(4)
    first.metric("pH", _display_number(result.ph))
    second.metric(
        "Ionic strength",
        f"{_display_number(result.ionic_strength_molal)} mol/kg",
    )
    third.metric("Water activity", _display_number(result.water_activity))
    fourth.metric("Osmotic coefficient", _display_number(result.osmotic_coefficient))

    summary_tab, species_tab, mean_tab, method_tab = st.tabs(
        ["Summary", "Aqueous species", "Mean coefficients", "Method & versions"]
    )

    with summary_tab:
        st.dataframe(
            [
                {"Quantity": "Temperature", "Value": result.temperature_c, "Unit": "°C"},
                {"Quantity": "Pressure", "Value": result.pressure_atm, "Unit": "atm"},
                {
                    "Quantity": "Alkalinity",
                    "Value": result.alkalinity_eq_per_kgw,
                    "Unit": "eq/kg H₂O",
                },
                {
                    "Quantity": "Charge balance",
                    "Value": result.charge_balance_eq,
                    "Unit": "eq",
                },
                {
                    "Quantity": "Charge-balance error",
                    "Value": result.charge_balance_error_percent,
                    "Unit": "%",
                },
            ],
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "No charge correction was applied. The reported composition is exactly the "
            "submitted composition on a molality basis."
        )

    with species_tab:
        st.caption(
            "All active aqueous solute species generated from the exposed analytical "
            "components. Downloaded values retain greater numerical precision."
        )
        st.dataframe(_species_rows(result), hide_index=True, width="stretch")

    with mean_tab:
        if result.mean_activity_coefficients:
            st.dataframe(
                [
                    {"Electrolyte": item.label, "Mean activity coefficient γ±": item.value}
                    for item in result.mean_activity_coefficients
                ],
                hide_index=True,
                width="stretch",
            )
        else:
            st.info("No curated mean coefficient is defined for the active ion pairs.")
        st.caption(
            "Mean coefficients are shown only for curated database definitions whose cation "
            "and anion are both present in the equilibrium solution."
        )

    with method_tab:
        st.markdown(
            """
            - **Activity model:** Pitzer only
            - **Individual-ion convention:** MacInnes scaling
            - **Boundary:** known pH, closed aqueous system
            - **Pressure:** fixed at 1 atm
            - **Redox:** disabled; no redox-sensitive components are exposed
            - **Solids and gases:** no phase equilibration or precipitation
            """
        )
        st.code(f"PHREEQC {result.engine_version}")
        st.code(f"pitzer.dat SHA-256: {result.database_sha256}")

    st.markdown("#### Downloads")
    _render_downloads(solution, result, warnings)


def render_app() -> None:
    apply_styles()

    st.title(APP_NAME)
    st.markdown(f"<p class='app-tagline'>{APP_TAGLINE}</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Current scientific scope")
        st.info(
            "Beta workflow: known pH, closed aqueous system, core major ions, 0–100 °C, "
            "and fixed pressure of 1 atm."
        )
        st.warning(
            "Results are not yet independently validated across the full range. Do not use "
            "this beta as the sole basis for safety-critical or regulatory decisions."
        )
        st.caption(
            "Individual-ion activity coefficients use the MacInnes convention and are "
            "convention-dependent."
        )

    with st.form("solution_form"):
        st.subheader("Solution definition")
        st.caption(
            "Enter analytical component totals. PHREEQC calculates the equilibrium species "
            "distribution; entered totals are not free-ion concentrations."
        )
        left, middle, right = st.columns(3)
        with left:
            ph = st.number_input("Known pH", min_value=-2.0, max_value=16.0, value=7.0)
        with middle:
            temperature_c = st.number_input(
                "Temperature [°C]", min_value=0.0, max_value=100.0, value=25.0
            )
        with right:
            unit = st.selectbox(
                "Composition unit",
                options=list(ConcentrationUnit),
                format_func=lambda item: item.display_label,
            )

        st.markdown("#### Composition")
        raw_components = _composition_inputs(unit)
        submitted = st.form_submit_button("Calculate with Pitzer", type="primary")

    if not submitted:
        st.caption("A balanced 0.1 mol/kg NaCl example is prefilled to get you started.")
        return

    solution = SolutionInput(
        ph=ph,
        temperature_c=temperature_c,
        components_molal=convert_composition_to_molal(raw_components, unit),
    )

    try:
        report = validate_solution(solution)
        for warning in report.warnings:
            st.warning(warning)
        with st.spinner("Running the PHREEQC Pitzer model…"):
            result = calculate_solution(solution)
    except (InputValidationError, CalculationError) as exc:
        st.error(str(exc))
        return

    _render_results(solution, result, report.warnings)
