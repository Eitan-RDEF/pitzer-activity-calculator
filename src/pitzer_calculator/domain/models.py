"""Typed inputs and outputs shared by the UI and calculation engine."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum


class ConcentrationUnit(str, Enum):
    """Composition units accepted by the version 1 interface."""

    MOL_PER_KGW = "mol/kg H2O"
    MMOL_PER_KGW = "mmol/kg H2O"

    @property
    def to_molal_factor(self) -> float:
        """Return the multiplier that converts this unit to mol/kg water."""

        return 1.0 if self is ConcentrationUnit.MOL_PER_KGW else 1e-3

    @property
    def display_label(self) -> str:
        """Return the Unicode label used in user-facing controls and tables."""

        return self.value.replace("H2O", "H₂O")


def convert_composition_to_molal(
    components: Mapping[str, float], unit: ConcentrationUnit
) -> dict[str, float]:
    """Convert a user composition to the engine's mol/kg-water basis."""

    return {key: value * unit.to_molal_factor for key, value in components.items()}


@dataclass(frozen=True, slots=True)
class SolutionInput:
    """A known-pH, closed aqueous solution expressed on a molality basis."""

    ph: float
    temperature_c: float
    components_molal: Mapping[str, float] = field(default_factory=dict)
    pressure_atm: float = 1.0


@dataclass(frozen=True, slots=True)
class SpeciesResult:
    """Equilibrium properties for one aqueous solute species."""

    name: str
    charge: int
    molality: float
    activity: float
    activity_coefficient: float
    log10_molality: float
    log10_activity: float
    log10_activity_coefficient: float


@dataclass(frozen=True, slots=True)
class MeanActivityCoefficient:
    """Stoichiometric mean activity coefficient for a curated electrolyte."""

    key: str
    label: str
    value: float


@dataclass(frozen=True, slots=True)
class CalculationResult:
    """Complete result contract for the known-pH, closed-system workflow."""

    ph: float
    temperature_c: float
    pressure_atm: float
    ionic_strength_molal: float
    alkalinity_eq_per_kgw: float
    water_mass_kg: float
    water_activity: float
    osmotic_coefficient: float
    charge_balance_eq: float
    charge_balance_error_percent: float
    species: tuple[SpeciesResult, ...]
    mean_activity_coefficients: tuple[MeanActivityCoefficient, ...]
    engine_version: str
    database_sha256: str
    phreeqc_input: str

    def species_by_name(self, name: str) -> SpeciesResult:
        """Return an active species or raise a clear lookup error."""

        for item in self.species:
            if item.name == name:
                return item
        raise KeyError(f"Species not present in this result: {name}")

    @property
    def charge_balance_status(self) -> str:
        """Classify absolute charge-balance error using the documented UI thresholds."""

        absolute_error = abs(self.charge_balance_error_percent)
        if absolute_error <= 2:
            return "good"
        if absolute_error <= 5:
            return "review"
        return "significant"

    @property
    def h_activity_coefficient(self) -> float:
        """Compatibility convenience for the original H+-only result."""

        return self.species_by_name("H+").activity_coefficient

    @property
    def h_activity(self) -> float:
        """Compatibility convenience for the original H+-only result."""

        return self.species_by_name("H+").activity
