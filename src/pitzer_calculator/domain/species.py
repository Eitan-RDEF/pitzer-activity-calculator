"""Audited component, species, and electrolyte metadata for the core workflow."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ComponentDefinition:
    key: str
    label: str
    phreeqc_name: str
    group: str
    default_molal: float = 0.0
    included_forms: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AqueousSpeciesDefinition:
    name: str
    charge: int


@dataclass(frozen=True, slots=True)
class MeanElectrolyteDefinition:
    key: str
    label: str
    cation: str
    anion: str


# The first complete workflow deliberately exposes only the major-ion core identified by
# the database audit. Conditional components remain documented but are not yet public inputs.
COMPONENTS: tuple[ComponentDefinition, ...] = (
    ComponentDefinition("Na", "Na⁺", "Na", "Cations", 0.1),
    ComponentDefinition("K", "K⁺", "K", "Cations"),
    ComponentDefinition("Ca", "Ca²⁺", "Ca", "Cations"),
    ComponentDefinition("Mg", "Mg²⁺", "Mg", "Cations"),
    ComponentDefinition("Cl", "Cl⁻", "Cl", "Anions and totals", 0.1),
    ComponentDefinition(
        "SO4",
        "Total S(VI)",
        "S(6)",
        "Anions and totals",
        included_forms=("SO₄²⁻", "HSO₄⁻"),
    ),
    ComponentDefinition(
        "C4",
        "Total inorganic C(IV)",
        "C(4)",
        "Anions and totals",
        included_forms=("CO₂(aq)", "HCO₃⁻", "CO₃²⁻", "MgCO₃(aq)"),
    ),
)

COMPONENT_BY_KEY = {component.key: component for component in COMPONENTS}


# Complete non-water species set that can be generated from the exposed components and pH
# by this exact database. Species with zero calculated molality are omitted from results.
AQUEOUS_SPECIES: tuple[AqueousSpeciesDefinition, ...] = (
    AqueousSpeciesDefinition("H+", 1),
    AqueousSpeciesDefinition("OH-", -1),
    AqueousSpeciesDefinition("Na+", 1),
    AqueousSpeciesDefinition("K+", 1),
    AqueousSpeciesDefinition("Mg+2", 2),
    AqueousSpeciesDefinition("Ca+2", 2),
    AqueousSpeciesDefinition("Cl-", -1),
    AqueousSpeciesDefinition("SO4-2", -2),
    AqueousSpeciesDefinition("HSO4-", -1),
    AqueousSpeciesDefinition("CO3-2", -2),
    AqueousSpeciesDefinition("HCO3-", -1),
    AqueousSpeciesDefinition("CO2", 0),
    AqueousSpeciesDefinition("MgOH+", 1),
    AqueousSpeciesDefinition("MgCO3", 0),
)


MEAN_ELECTROLYTES: tuple[MeanElectrolyteDefinition, ...] = (
    MeanElectrolyteDefinition("NaCl", "NaCl", "Na+", "Cl-"),
    MeanElectrolyteDefinition("KCl", "KCl", "K+", "Cl-"),
    MeanElectrolyteDefinition("CaCl2", "CaCl₂", "Ca+2", "Cl-"),
    MeanElectrolyteDefinition("MgCl2", "MgCl₂", "Mg+2", "Cl-"),
    MeanElectrolyteDefinition("Na2SO4", "Na₂SO₄", "Na+", "SO4-2"),
)
