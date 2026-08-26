import os

import pytest

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

