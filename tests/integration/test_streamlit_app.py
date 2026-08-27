import os
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pitzer_calculator.domain.models import ConcentrationUnit

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the Streamlit calculation smoke test.",
)


def test_entered_nacl_workflow_renders_complete_results() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    assert not app.exception
    assert any(
        "Calculate activities in concentrated aqueous solutions" in item.value
        for item in app.markdown
    )
    assert any("Eitan Elfassy" in item.value for item in app.caption)
    rendered_markdown = "\n".join(item.value for item in app.markdown)
    assert "Version 1.0.0" in rendered_markdown
    assert "docs/validation-status.md" in rendered_markdown
    assert "docs/supported-components.md" in rendered_markdown
    assert "PRIVACY.md" in rendered_markdown
    assert "docs/third-party-notices.md" in rendered_markdown
    assert "Beta" not in rendered_markdown
    assert any("Includes: SO₄²⁻, HSO₄⁻" in item.value for item in app.caption)
    assert any(
        "Includes: CO₂(aq), HCO₃⁻, CO₃²⁻, MgCO₃(aq)" in item.value
        for item in app.caption
    )
    assert any(
        item.label == "Anions and acid–base components" for item in app.expander
    )
    component_inputs = [
        item for item in app.number_input if item.key.startswith("component_")
    ]
    assert component_inputs and all(item.value == 0.0 for item in component_inputs)
    app.number_input(key="component_MOL_PER_KGW_Na").set_value(0.1)
    app.number_input(key="component_MOL_PER_KGW_Cl").set_value(0.1)
    app.button[0].click().run(timeout=20)

    assert not app.exception
    assert len(app.metric) == 4
    assert app.metric[1].label == "Ionic strength (mol/kg H₂O)"
    assert "mol/kg" not in app.metric[1].value
    assert len(app.dataframe) == 3
    assert any("Explore results" in item.value for item in app.markdown)
    assert [tab.label for tab in app.tabs] == [
        "Mean coefficients",
        "Aqueous species",
        "Conditions & balance",
        "Method & versions",
    ]
    download_buttons = app.get("download_button")
    assert [item.proto.label for item in download_buttons] == [
        "Species CSV",
        "PHREEQC input",
        "Calculation report",
        "Complete ZIP",
    ]
    assert all(item.proto.ignore_rerun for item in download_buttons)


def test_reset_clears_composition_and_restores_physical_defaults() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    app.number_input(key="solution_ph").set_value(9.0)
    app.number_input(key="solution_temperature_c").set_value(60.0)
    app.number_input(key="component_MOL_PER_KGW_Na").set_value(0.5)
    app.get("button")[1].click().run(timeout=20)

    assert not app.exception
    assert app.number_input(key="solution_ph").value == 7.0
    assert app.number_input(key="solution_temperature_c").value == 25.0
    assert app.selectbox(key="composition_unit").value == ConcentrationUnit.MOL_PER_KGW
    component_values = [
        item.value for item in app.number_input if item.key.startswith("component_")
    ]
    assert component_values and all(value == 0.0 for value in component_values)
    assert not app.metric


def test_reference_case_selection_prefills_existing_form_and_shows_source_data() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    app.selectbox(key="reference_case_id").select(
        "nist_thermoml_2012_cacl2_0p5m_25c"
    ).run(timeout=20)

    assert not app.exception
    assert app.number_input(key="solution_ph").value == 7.0
    assert app.number_input(key="solution_temperature_c").value == 25.0
    assert app.selectbox(key="composition_unit").value == ConcentrationUnit.MOL_PER_KGW
    assert app.number_input(key="component_MOL_PER_KGW_Ca").value == 0.5
    assert app.number_input(key="component_MOL_PER_KGW_Cl").value == 1.0
    assert app.number_input(key="component_MOL_PER_KGW_Na").value == 0.0
    assert any(
        item.label == "Load a published reference case (optional)"
        for item in app.expander
    )
    rendered_markdown = "\n".join(item.value for item in app.markdown)
    assert "Independent experimental/evaluated reference" in rendered_markdown
    assert [item.label for item in app.toggle] == [
        "Show published values and source",
        "Show mapping assumptions and limitations",
    ]
    assert all(not item.value for item in app.toggle)
    assert "Partanen, J. I. (2012)" not in rendered_markdown
    assert not app.dataframe

    app.toggle(key="show_reference_source").set_value(True).run(timeout=20)

    assert not app.exception
    rendered_markdown = "\n".join(item.value for item in app.markdown)
    assert "Partanen, J. I. (2012)" in rendered_markdown
    assert len(app.dataframe) == 1

    app.toggle(key="show_reference_assumptions").set_value(True).run(timeout=20)

    assert not app.exception
    rendered_markdown = "\n".join(item.value for item in app.markdown)
    assert "source defines a binary CaCl2-water system" in rendered_markdown


def test_conditional_component_limitations_and_active_warnings_are_visible() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    assert app.number_input(key="component_MOL_PER_KGW_Ba")
    assert any(
        "Sulfate and carbonate coverage is weak" in item.value for item in app.caption
    )

    app.number_input(key="component_MOL_PER_KGW_Ba").set_value(0.001)
    app.number_input(key="component_MOL_PER_KGW_SO4").set_value(0.01)
    app.button[0].click().run(timeout=20)

    assert not app.exception
    rendered_warnings = "\n".join(item.value for item in app.warning)
    assert "Ba²⁺ has conditional database coverage" in rendered_warnings
    assert "does not equilibrate solids" in rendered_warnings
