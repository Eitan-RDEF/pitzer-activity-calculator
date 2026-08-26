import os
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pitzer_calculator.domain.models import ConcentrationUnit

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the Streamlit calculation smoke test.",
)


def test_default_nacl_workflow_renders_complete_results() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    assert not app.exception
    assert any(
        "Calculate activities in concentrated aqueous solutions" in item.value
        for item in app.markdown
    )
    assert any("Eitan Elfassy" in item.value for item in app.caption)
    assert any("Includes: SO₄²⁻, HSO₄⁻" in item.value for item in app.caption)
    assert any(
        "Includes: CO₂(aq), HCO₃⁻, CO₃²⁻, MgCO₃(aq)" in item.value
        for item in app.caption
    )
    app.button[0].click().run(timeout=20)

    assert not app.exception
    assert len(app.metric) == 4
    assert len(app.dataframe) == 3


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
