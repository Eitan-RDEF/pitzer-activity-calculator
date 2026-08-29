"""Validated browser-resume state for inactivity suspension.

The gateway keeps this payload in ``sessionStorage`` for the lifetime of one browser tab.
When the Streamlit iframe is recreated, the gateway sends the payload once in a short-lived
same-origin cookie.  This module accepts only the documented form schema before copying values
into Streamlit session state.
"""

from __future__ import annotations

import base64
import json
import math
from collections.abc import Mapping, Set
from typing import Any

from pitzer_calculator.domain.models import ConcentrationUnit
from pitzer_calculator.domain.species import COMPONENTS

BROWSER_STATE_VERSION = 1
RESUME_COOKIE_NAME = "pitzer_resume_state"
MAX_RESUME_COOKIE_LENGTH = 4096


def component_widget_key(unit: ConcentrationUnit, component_key: str) -> str:
    """Return the stable Streamlit key for one unit-specific component input."""

    return f"component_{unit.name}_{component_key}"


def serialise_browser_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Return the compact, JSON-safe subset required to restore the calculator form."""

    unit = state.get("composition_unit", ConcentrationUnit.MOL_PER_KGW)
    if not isinstance(unit, ConcentrationUnit):
        unit = ConcentrationUnit.MOL_PER_KGW

    components: dict[str, dict[str, float]] = {}
    for candidate_unit in ConcentrationUnit:
        active_values: dict[str, float] = {}
        for component in COMPONENTS:
            value = _finite_float(
                state.get(component_widget_key(candidate_unit, component.key), 0.0)
            )
            if value is not None and value > 0:
                active_values[component.key] = value
        if active_values:
            components[candidate_unit.name] = active_values

    return {
        "version": BROWSER_STATE_VERSION,
        "ph": _bounded_float(state.get("solution_ph"), -2.0, 16.0, 7.0),
        "temperature_c": _bounded_float(
            state.get("solution_temperature_c"), 0.0, 100.0, 25.0
        ),
        "unit": unit.name,
        "reference_case_id": str(state.get("reference_case_id", "")),
        "components": components,
        "calculation_current": bool(state.get("_calculation_current", False)),
    }


def decode_resume_cookie(
    encoded: str | None,
    *,
    valid_reference_ids: Set[str],
) -> dict[str, Any] | None:
    """Decode and validate the one-time state transfer supplied by the gateway."""

    if not encoded or len(encoded) > MAX_RESUME_COOKIE_LENGTH:
        return None

    try:
        padding = "=" * (-len(encoded) % 4)
        raw = base64.urlsafe_b64decode(f"{encoded}{padding}").decode("utf-8")
        payload = json.loads(raw)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict) or payload.get("version") != BROWSER_STATE_VERSION:
        return None

    ph = _bounded_float(payload.get("ph"), -2.0, 16.0)
    temperature_c = _bounded_float(payload.get("temperature_c"), 0.0, 100.0)
    unit_name = payload.get("unit")
    if ph is None or temperature_c is None or not isinstance(unit_name, str):
        return None

    try:
        unit = ConcentrationUnit[unit_name]
    except KeyError:
        return None

    restored: dict[str, Any] = {
        "solution_ph": ph,
        "solution_temperature_c": temperature_c,
        "composition_unit": unit,
        "reference_case_id": "",
        "show_reference_source": False,
        "show_reference_assumptions": False,
        "_calculation_current": bool(payload.get("calculation_current", False)),
    }
    reference_case_id = payload.get("reference_case_id")
    if isinstance(reference_case_id, str) and reference_case_id in valid_reference_ids:
        restored["reference_case_id"] = reference_case_id

    for candidate_unit in ConcentrationUnit:
        for component in COMPONENTS:
            restored[component_widget_key(candidate_unit, component.key)] = 0.0

    components = payload.get("components", {})
    if not isinstance(components, dict):
        return None
    known_component_keys = {component.key for component in COMPONENTS}
    for candidate_unit_name, candidate_values in components.items():
        if not isinstance(candidate_unit_name, str) or not isinstance(candidate_values, dict):
            return None
        try:
            candidate_unit = ConcentrationUnit[candidate_unit_name]
        except KeyError:
            return None
        for component_key, raw_value in candidate_values.items():
            if component_key not in known_component_keys:
                return None
            value = _finite_float(raw_value)
            if value is None or value < 0:
                return None
            restored[component_widget_key(candidate_unit, component_key)] = value

    return restored


def _finite_float(value: Any) -> float | None:
    """Coerce a finite numeric value while rejecting booleans and malformed input."""

    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _bounded_float(
    value: Any,
    minimum: float,
    maximum: float,
    fallback: float | None = None,
) -> float | None:
    """Return a finite value inside the inclusive range, otherwise ``fallback``."""

    number = _finite_float(value)
    if number is None or not minimum <= number <= maximum:
        return fallback
    return number
