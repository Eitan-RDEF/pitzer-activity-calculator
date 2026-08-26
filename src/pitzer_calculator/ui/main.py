"""Streamlit composition for the complete core calculation workflow."""

from typing import Any

import streamlit as st

from pitzer_calculator import __version__
from pitzer_calculator.config import APP_NAME, APP_TAGLINE
from pitzer_calculator.domain.models import (
    ConcentrationUnit,
    SolutionInput,
    convert_composition_to_molal,
)
from pitzer_calculator.domain.species import (
    ANION_ACID_BASE_GROUP,
    CATION_GROUP,
    COMPONENTS,
    CONDITIONAL_COMPONENTS,
    CORE_COMPONENTS,
    ComponentDefinition,
)
from pitzer_calculator.engine.exports import (
    calculation_bundle,
    calculation_report,
    species_csv,
)
from pitzer_calculator.engine.phreeqc import CalculationError, calculate_solution
from pitzer_calculator.engine.validation import InputValidationError, validate_solution
from pitzer_calculator.reference_cases import (
    ReferenceCase,
    load_reference_cases,
    published_output_rows,
)
from pitzer_calculator.ui.styles import apply_styles

MANUAL_COMPOSITION = ""


def _display_number(value: float, significant_digits: int = 6) -> str:
    return format(value, f".{significant_digits}g")


def _reset_solution_form() -> None:
    """Restore physical inputs and clear every unit-specific composition widget."""

    st.session_state["reference_case_id"] = MANUAL_COMPOSITION
    st.session_state["show_reference_source"] = False
    st.session_state["show_reference_assumptions"] = False
    st.session_state["solution_ph"] = 7.0
    st.session_state["solution_temperature_c"] = 25.0
    st.session_state["composition_unit"] = ConcentrationUnit.MOL_PER_KGW
    for unit in ConcentrationUnit:
        for component in COMPONENTS:
            st.session_state[f"component_{unit.name}_{component.key}"] = 0.0


def _apply_reference_case(cases_by_id: dict[str, ReferenceCase]) -> None:
    """Prefill the existing form when the user selects a reviewed reference case."""

    selected_id = st.session_state.get("reference_case_id", MANUAL_COMPOSITION)
    st.session_state["show_reference_source"] = False
    st.session_state["show_reference_assumptions"] = False
    if selected_id == MANUAL_COMPOSITION:
        return

    case = cases_by_id[selected_id]
    st.session_state["solution_ph"] = case.known_ph
    st.session_state["solution_temperature_c"] = case.temperature_c
    st.session_state["composition_unit"] = ConcentrationUnit.MOL_PER_KGW
    for unit in ConcentrationUnit:
        for component in COMPONENTS:
            st.session_state[f"component_{unit.name}_{component.key}"] = 0.0
    for component, value in case.components_molal.items():
        st.session_state[f"component_MOL_PER_KGW_{component}"] = value


def _reference_output_table(case: ReferenceCase) -> list[dict[str, Any]]:
    return [
        {
            "Published property": row.property,
            "Published value": _display_number(row.value),
            "Expanded uncertainty (95%)": (
                _display_number(row.expanded_uncertainty_95)
                if row.expanded_uncertainty_95 is not None
                else "—"
            ),
            "Unit": row.unit,
        }
        for row in published_output_rows(case)
    ]


def _render_reference_selector(cases: tuple[ReferenceCase, ...]) -> None:
    """Render optional case selection and compact source information."""

    cases_by_id = {case.id: case for case in cases}
    options = [MANUAL_COMPOSITION, *cases_by_id]

    with st.expander("Load a published reference case (optional)"):
        st.caption(
            f"Optionally load one of {len(cases)} reviewed compositions. You still run the "
            "normal calculation and interpret the published values yourself."
        )
        selected_id = st.selectbox(
            "Reference case",
            options=options,
            format_func=lambda case_id: (
                "Manual composition"
                if case_id == MANUAL_COMPOSITION
                else f"{cases_by_id[case_id].evidence_label} · {cases_by_id[case_id].title}"
            ),
            key="reference_case_id",
            on_change=_apply_reference_case,
            args=(cases_by_id,),
            help="Selecting a case prefills the existing known-pH calculation form.",
        )

        if selected_id == MANUAL_COMPOSITION:
            st.caption(
                "Choose a case to load its composition and inspect its published source "
                "values."
            )
            return

        case = cases_by_id[selected_id]
        st.markdown(f"**{case.evidence_label}** — {case.description}")
        st.caption(
            "You may edit the loaded inputs, but the reference values below always describe "
            "the original published case."
        )

        show_source = st.toggle(
            "Show published values and source",
            key="show_reference_source",
        )
        if show_source:
            st.dataframe(
                _reference_output_table(case),
                hide_index=True,
                width="stretch",
            )
            st.markdown(f"**Citation:** {case.source.citation}")
            st.markdown(f"**Source location:** {case.source.locator}")
            st.markdown(f"[Open the published source]({case.source.url})")
            if case.source.license_url:
                st.markdown(f"[Source reuse terms]({case.source.license_url})")
            st.caption(
                "These are published source values, not automatically calculated "
                "differences, tolerances, or pass/fail criteria."
            )

        show_assumptions = st.toggle(
            "Show mapping assumptions and limitations",
            key="show_reference_assumptions",
        )
        if show_assumptions:
            st.markdown("\n".join(f"- {item}" for item in case.assumptions))


def _component_grid(
    components: tuple[ComponentDefinition, ...],
    unit: ConcentrationUnit,
    columns_per_row: int = 4,
) -> dict[str, float]:
    values: dict[str, float] = {}
    for row_start in range(0, len(components), columns_per_row):
        columns = st.columns(columns_per_row)
        for column, component in zip(
            columns,
            components[row_start : row_start + columns_per_row],
            strict=False,
        ):
            with column:
                default = component.default_molal / unit.to_molal_factor
                widget_key = f"component_{unit.name}_{component.key}"
                default_arguments = (
                    {"value": default} if widget_key not in st.session_state else {}
                )
                values[component.key] = st.number_input(
                    f"{component.label} [{unit.display_label}]",
                    min_value=0.0,
                    format="%.8g",
                    key=widget_key,
                    **default_arguments,
                )
                if component.included_forms:
                    st.caption(f"Includes: {', '.join(component.included_forms)}")
                if component.limitation:
                    st.caption(f"Conditional: {component.limitation}")
    return values


def _composition_inputs(unit: ConcentrationUnit) -> dict[str, float]:
    values: dict[str, float] = {}
    for group in (CATION_GROUP, ANION_ACID_BASE_GROUP):
        with st.expander(group, expanded=True):
            group_components = tuple(item for item in CORE_COMPONENTS if item.group == group)
            values.update(
                _component_grid(group_components, unit)
            )

    with st.expander("Extended components — conditional database coverage"):
        st.caption(
            "These components are calculated by the bundled database, but their interaction "
            "coverage is less complete. Active limitations are repeated with the results."
        )
        for group in (CATION_GROUP, ANION_ACID_BASE_GROUP):
            st.markdown(f"**{group}**")
            group_components = tuple(
                item for item in CONDITIONAL_COMPONENTS if item.group == group
            )
            values.update(_component_grid(group_components, unit))
        st.info(
            "Fe(III) and Al are unavailable because this database does not define safe "
            "analytical inputs for them."
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
        "Ionic strength (mol/kg H₂O)",
        _display_number(result.ionic_strength_molal),
    )
    third.metric("Water activity", _display_number(result.water_activity))
    fourth.metric("Osmotic coefficient", _display_number(result.osmotic_coefficient))

    st.markdown(
        '<div class="results-view-label">Explore results</div>',
        unsafe_allow_html=True,
    )
    mean_tab, species_tab, summary_tab, method_tab = st.tabs(
        [
            "Mean coefficients",
            "Aqueous species",
            "Conditions & balance",
            "Method & versions",
        ]
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
            - **Redox:** disabled; Fe and Mn inputs remain fixed as Fe(II) and Mn(II)
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
    st.markdown(
        """
        <section class="app-introduction">
          <h2>Calculate activities in concentrated aqueous solutions</h2>
          <p>
            Enter the solution composition, pH, and temperature. The calculator uses the
            PHREEQC Pitzer model to determine equilibrium species, activities, activity
            coefficients, water properties, and charge-balance diagnostics.
          </p>
          <div class="workflow-steps" aria-label="Calculation workflow">
            <div><span>1</span><strong>Define</strong><small>Enter the solution</small></div>
            <div><span>2</span><strong>Calculate</strong><small>Run the Pitzer model</small></div>
            <div>
              <span>3</span><strong>Review</strong><small>Explore or download results</small>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Quick start")
        st.markdown(
            """
            <div class="quick-start-list">
              <ol>
                <li>Enter analytical component totals.</li>
                <li>Set the known pH and temperature.</li>
                <li>Calculate and review the charge balance.</li>
                <li>Explore or download the results.</li>
              </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="validation-note">
              <strong>Version {__version__}</strong>
              <span>
                Selected outputs have been compared with published USGS and NIST reference
                data. Independently verify results used for critical engineering decisions.
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Calculation assumptions"):
            st.markdown(
                """
                - Pitzer activity model
                - Molality concentration basis
                - Known-pH, closed aqueous system
                - Fixed pressure: 1 atm
                - MacInnes convention for individual ions
                - No gas, mineral, or redox equilibrium; Fe/Mn remain fixed as +II
                """
            )
        with st.expander("Learn more"):
            st.markdown(
                """
                - [Scientific method](https://github.com/Eitan-RDEF/pitzer-activity-calculator/blob/main/docs/scientific-method.md)
                - [Supported components](https://github.com/Eitan-RDEF/pitzer-activity-calculator/blob/main/docs/supported-components.md)
                - [Validation evidence](https://github.com/Eitan-RDEF/pitzer-activity-calculator/blob/main/docs/validation-status.md)
                - [Privacy and contact](https://github.com/Eitan-RDEF/pitzer-activity-calculator/blob/main/PRIVACY.md)
                - [License and third-party notices](https://github.com/Eitan-RDEF/pitzer-activity-calculator/blob/main/docs/third-party-notices.md)
                - [Source code on GitHub](https://github.com/Eitan-RDEF/pitzer-activity-calculator)
                """
            )
        st.divider()
        st.caption(
            "Free and open-source engineering tool developed by "
            "[Eitan Elfassy](mailto:eitan.elfassi@gmail.com)."
        )

    _render_reference_selector(load_reference_cases())

    with st.form("solution_form"):
        st.subheader("Solution definition")
        st.caption(
            "Enter analytical component totals. PHREEQC calculates the equilibrium species "
            "distribution; entered totals are not free-ion concentrations."
        )
        left, middle, right, _physical_spacer = st.columns(4)
        with left:
            ph_default = {"value": 7.0} if "solution_ph" not in st.session_state else {}
            ph = st.number_input(
                "Known pH",
                min_value=-2.0,
                max_value=16.0,
                key="solution_ph",
                **ph_default,
            )
        with middle:
            temperature_default = (
                {"value": 25.0}
                if "solution_temperature_c" not in st.session_state
                else {}
            )
            temperature_c = st.number_input(
                "Temperature [°C]",
                min_value=0.0,
                max_value=100.0,
                key="solution_temperature_c",
                **temperature_default,
            )
        with right:
            unit = st.selectbox(
                "Composition unit",
                options=list(ConcentrationUnit),
                format_func=lambda item: item.display_label,
                key="composition_unit",
            )

        st.markdown("#### Composition")
        raw_components = _composition_inputs(unit)
        calculate_column, reset_column, _spacer = st.columns([1.35, 0.75, 3.4])
        with calculate_column:
            submitted = st.form_submit_button(
                "Calculate with Pitzer", type="primary", width="stretch"
            )
        with reset_column:
            reset_requested = st.form_submit_button(
                "Reset",
                on_click=_reset_solution_form,
                width="stretch",
            )

    if reset_requested:
        st.caption("Inputs cleared. Physical conditions were restored to their defaults.")
        return

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
