import os

import pytest

from pitzer_calculator.config import DEFAULT_DATABASE_PATH
from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.engine.phreeqc import calculate_h_activity

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the native PHREEQC smoke test.",
)


def test_calculates_balanced_nacl_solution() -> None:
    result = calculate_h_activity(
        SolutionInput(
            ph=7.0,
            temperature_c=25.0,
            components_molal={"Na": 0.1, "Cl": 0.1},
        )
    )

    assert result.ionic_strength_molal > 0
    assert result.h_activity_coefficient > 0


def test_database_exposes_mean_gamma_and_water_properties() -> None:
    """Pin direct PHREEQC functions needed by the planned full result model."""
    from phreeqc import Phreeqc

    phreeqc = Phreeqc()
    assert phreeqc.LoadDatabase(str(DEFAULT_DATABASE_PATH)) == 0
    input_text = """\
SOLUTION 1
    temp 25
    units mol/kgw
    Na 1
    Cl 1

SELECTED_OUTPUT
    -reset false

USER_PUNCH
    -headings mean_nacl water_activity osmotic_coefficient
    10 PUNCH MEANG("NaCl")
    20 PUNCH ACT("H2O")
    30 PUNCH OSMOTIC

END
"""
    assert phreeqc.RunString(input_text) == 0, phreeqc.GetErrorString()
    output = phreeqc.GetSelectedOutput()

    assert output["mean_nacl"][0] == pytest.approx(0.657220, rel=1e-5)
    assert output["water_activity"][0] == pytest.approx(0.966825, rel=1e-5)
    assert output["osmotic_coefficient"][0] == pytest.approx(0.936359, rel=1e-5)
