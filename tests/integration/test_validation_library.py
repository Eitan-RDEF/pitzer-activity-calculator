import json
import os
from pathlib import Path
from typing import Any

import pytest

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.engine.phreeqc import calculate_solution

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LIBRARY_PATH = REPOSITORY_ROOT / "data" / "examples" / "validation_library.json"
CASES: list[dict[str, Any]] = json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))["cases"]

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the native PHREEQC smoke test.",
)


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_reference_case_input_runs_through_the_normal_engine(case: dict[str, Any]) -> None:
    inputs = case["input"]
    result = calculate_solution(
        SolutionInput(
            ph=inputs["known_ph"],
            temperature_c=inputs["temperature_c"],
            pressure_atm=inputs["pressure_atm"],
            components_molal=inputs["components"],
        )
    )

    published_mean_keys = set(
        case["published_outputs"].get("mean_activity_coefficients", {})
    )
    calculated_mean_keys = {coefficient.key for coefficient in result.mean_activity_coefficients}

    assert result.water_activity > 0
    assert result.osmotic_coefficient > 0
    assert result.ionic_strength_molal > 0
    assert published_mean_keys <= calculated_mean_keys
