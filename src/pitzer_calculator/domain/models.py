"""Typed inputs and outputs shared by the UI and calculation engine."""

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SolutionInput:
    """A single aqueous solution expressed on a molality basis."""

    ph: float
    temperature_c: float
    components_molal: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CalculationResult:
    """Initial H+ activity result returned by the PHREEQC adapter."""

    ph: float
    ionic_strength_molal: float
    charge_balance_error_percent: float
    log10_h_activity: float
    log10_h_molality: float
    log10_h_activity_coefficient: float
    h_activity_coefficient: float
    h_molality: float
    h_activity: float
    phreeqc_input: str
