import base64
import json

from pitzer_calculator.domain.models import ConcentrationUnit
from pitzer_calculator.ui.browser_state import (
    BROWSER_STATE_VERSION,
    component_widget_key,
    decode_resume_cookie,
    serialise_browser_state,
)


def _encode(payload: object) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def test_browser_state_round_trip_restores_only_known_form_values() -> None:
    state = {
        "solution_ph": 8.25,
        "solution_temperature_c": 45.0,
        "composition_unit": ConcentrationUnit.MMOL_PER_KGW,
        "reference_case_id": "reviewed-case",
        "component_MOL_PER_KGW_Na": 0.1,
        "component_MMOL_PER_KGW_Cl": 125.0,
        "_calculation_current": True,
    }

    payload = serialise_browser_state(state)
    restored = decode_resume_cookie(
        _encode(payload),
        valid_reference_ids={"reviewed-case"},
    )

    assert restored is not None
    assert restored["solution_ph"] == 8.25
    assert restored["solution_temperature_c"] == 45.0
    assert restored["composition_unit"] is ConcentrationUnit.MMOL_PER_KGW
    assert restored["reference_case_id"] == "reviewed-case"
    assert restored[component_widget_key(ConcentrationUnit.MOL_PER_KGW, "Na")] == 0.1
    assert restored[component_widget_key(ConcentrationUnit.MMOL_PER_KGW, "Cl")] == 125.0
    assert restored[component_widget_key(ConcentrationUnit.MOL_PER_KGW, "K")] == 0.0
    assert restored["_calculation_current"] is True


def test_invalid_or_unrecognised_resume_state_is_rejected() -> None:
    assert decode_resume_cookie("not-base64", valid_reference_ids=set()) is None
    assert decode_resume_cookie(
        _encode({"version": BROWSER_STATE_VERSION + 1}),
        valid_reference_ids=set(),
    ) is None
    assert decode_resume_cookie(
        _encode(
            {
                "version": BROWSER_STATE_VERSION,
                "ph": 7,
                "temperature_c": 25,
                "unit": "MOL_PER_KGW",
                "components": {"MOL_PER_KGW": {"unknown": 1}},
            }
        ),
        valid_reference_ids=set(),
    ) is None


def test_unknown_reference_case_is_restored_as_manual_composition() -> None:
    payload = {
        "version": BROWSER_STATE_VERSION,
        "ph": 7,
        "temperature_c": 25,
        "unit": "MOL_PER_KGW",
        "reference_case_id": "deleted-case",
        "components": {},
        "calculation_current": False,
    }

    restored = decode_resume_cookie(_encode(payload), valid_reference_ids=set())

    assert restored is not None
    assert restored["reference_case_id"] == ""
