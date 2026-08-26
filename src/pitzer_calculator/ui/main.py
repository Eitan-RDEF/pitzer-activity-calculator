"""Top-level Streamlit composition for the initial vertical slice."""

import streamlit as st

from pitzer_calculator.config import APP_NAME, APP_TAGLINE
from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.domain.species import COMPONENTS
from pitzer_calculator.engine.phreeqc import CalculationError, calculate_h_activity
from pitzer_calculator.engine.validation import InputValidationError, validate_solution
from pitzer_calculator.ui.styles import apply_styles


def _composition_inputs() -> dict[str, float]:
    values: dict[str, float] = {}
    for group in ("Cations", "Anions and totals"):
        with st.expander(group, expanded=True):
            columns = st.columns(3)
            group_components = [item for item in COMPONENTS if item.group == group]
            for index, component in enumerate(group_components):
                with columns[index % len(columns)]:
                    values[component.key] = st.number_input(
                        f"{component.label} [mol/kg H₂O]",
                        min_value=0.0,
                        value=0.0,
                        format="%.6g",
                        key=f"component_{component.key}",
                    )
    return values


def _render_results(result) -> None:
    st.subheader("Calculation results")
    first, second, third, fourth = st.columns(4)
    first.metric("γ(H⁺)", f"{result.h_activity_coefficient:.6g}")
    second.metric("H⁺ activity", f"{result.h_activity:.6g}")
    third.metric("Ionic strength", f"{result.ionic_strength_molal:.6g} mol/kg")
    fourth.metric("Charge-balance error", f"{result.charge_balance_error_percent:.3g}%")

    st.dataframe(
        [
            {"Quantity": "Calculated pH", "Value": result.ph, "Unit": ""},
            {"Quantity": "log₁₀ a(H⁺)", "Value": result.log10_h_activity, "Unit": ""},
            {"Quantity": "log₁₀ m(H⁺)", "Value": result.log10_h_molality, "Unit": ""},
            {
                "Quantity": "log₁₀ γ(H⁺)",
                "Value": result.log10_h_activity_coefficient,
                "Unit": "",
            },
            {"Quantity": "H⁺ molality", "Value": result.h_molality, "Unit": "mol/kg H₂O"},
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.caption("Identity check: a(H⁺) = γ(H⁺) × m(H⁺).")
    st.download_button(
        "Download reproducible PHREEQC input",
        data=result.phreeqc_input,
        file_name="pitzer_calculation.pqi",
        mime="text/plain",
    )


def render_app() -> None:
    apply_styles()

    st.title(APP_NAME)
    st.markdown(f"<p class='app-tagline'>{APP_TAGLINE}</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("Model notes")
        st.info(
            "This first vertical slice reproduces the original H⁺ activity calculation. "
            "The supported outputs and validation suite will expand before public release."
        )
        st.caption(
            "Individual-ion activity coefficients are convention-dependent. The PHREEQC "
            "Pitzer database uses the MacInnes convention by default."
        )

    with st.form("solution_form"):
        st.subheader("Solution definition")
        left, right = st.columns(2)
        with left:
            ph = st.number_input("pH", value=7.0, format="%.4f")
        with right:
            temperature_c = st.number_input("Temperature [°C]", value=25.0, format="%.2f")

        st.markdown("#### Composition")
        st.caption("Enter analytical totals on a molality basis. Leave absent components at zero.")
        components = _composition_inputs()
        submitted = st.form_submit_button("Calculate with Pitzer", type="primary")

    if not submitted:
        st.caption("Start with pH and temperature, then add the ions present in the solution.")
        return

    solution = SolutionInput(
        ph=ph,
        temperature_c=temperature_c,
        components_molal=components,
    )

    try:
        report = validate_solution(solution)
        for warning in report.warnings:
            st.warning(warning)
        with st.spinner("Running PHREEQC Pitzer calculation…"):
            result = calculate_h_activity(solution)
    except (InputValidationError, CalculationError) as exc:
        st.error(str(exc))
        return

    _render_results(result)

