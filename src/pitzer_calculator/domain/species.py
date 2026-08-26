"""Audited component, species, and electrolyte metadata for the core workflow."""

from dataclasses import dataclass
from enum import Enum


class ComponentSupport(str, Enum):
    """Product-facing confidence tier for an exposed analytical component."""

    CORE = "core"
    CONDITIONAL = "conditional"


@dataclass(frozen=True, slots=True)
class ComponentDefinition:
    key: str
    label: str
    phreeqc_name: str
    group: str
    default_molal: float = 0.0
    included_forms: tuple[str, ...] = ()
    support: ComponentSupport = ComponentSupport.CORE
    limitation: str | None = None


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


# Core inputs are shown by default. Conditional inputs are exposed in a separate advanced
# section with their audited database limitations repeated in calculation warnings.
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
    ComponentDefinition(
        "Li",
        "Li⁺",
        "Li",
        "Cations",
        support=ComponentSupport.CONDITIONAL,
        limitation=(
            "Useful for brines, but carbonate, bicarbonate, and bisulfate interactions "
            "are incomplete."
        ),
    ),
    ComponentDefinition(
        "Sr",
        "Sr²⁺",
        "Sr",
        "Cations",
        support=ComponentSupport.CONDITIONAL,
        limitation="Carbonate, hydroxide, and bisulfate interactions are incomplete.",
    ),
    ComponentDefinition(
        "Ba",
        "Ba²⁺",
        "Ba",
        "Cations",
        support=ComponentSupport.CONDITIONAL,
        limitation=(
            "Sulfate and carbonate coverage is weak; mineral precipitation is not modeled."
        ),
    ),
    ComponentDefinition(
        "Fe2",
        "Total Fe(II)",
        "Fe",
        "Cations",
        support=ComponentSupport.CONDITIONAL,
        limitation="Fixed Fe(II) only; no redox calculation or Fe(III) conversion is performed.",
    ),
    ComponentDefinition(
        "Mn2",
        "Total Mn(II)",
        "Mn",
        "Cations",
        support=ComponentSupport.CONDITIONAL,
        limitation="Fixed Mn(II) only; no redox calculation is performed.",
    ),
    ComponentDefinition(
        "Br",
        "Br⁻",
        "Br",
        "Anions and totals",
        support=ComponentSupport.CONDITIONAL,
        limitation="Good binary coverage, but fewer multicomponent interaction parameters.",
    ),
    ComponentDefinition(
        "B",
        "Total B",
        "B",
        "Anions and totals",
        support=ComponentSupport.CONDITIONAL,
        limitation="Several borate species are represented, but interaction coverage is uneven.",
    ),
    ComponentDefinition(
        "Si",
        "Total Si",
        "Si",
        "Anions and totals",
        support=ComponentSupport.CONDITIONAL,
        limitation=(
            "Neutral silica is better supported than deprotonated silicate species, "
            "especially at high pH."
        ),
    ),
)

COMPONENT_BY_KEY = {component.key: component for component in COMPONENTS}
CORE_COMPONENTS = tuple(
    component for component in COMPONENTS if component.support is ComponentSupport.CORE
)
CONDITIONAL_COMPONENTS = tuple(
    component for component in COMPONENTS if component.support is ComponentSupport.CONDITIONAL
)


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
    AqueousSpeciesDefinition("Br-", -1),
    AqueousSpeciesDefinition("Li+", 1),
    AqueousSpeciesDefinition("Sr+2", 2),
    AqueousSpeciesDefinition("Ba+2", 2),
    AqueousSpeciesDefinition("Fe+2", 2),
    AqueousSpeciesDefinition("Mn+2", 2),
    AqueousSpeciesDefinition("SO4-2", -2),
    AqueousSpeciesDefinition("HSO4-", -1),
    AqueousSpeciesDefinition("CO3-2", -2),
    AqueousSpeciesDefinition("HCO3-", -1),
    AqueousSpeciesDefinition("CO2", 0),
    AqueousSpeciesDefinition("MgOH+", 1),
    AqueousSpeciesDefinition("MgCO3", 0),
    AqueousSpeciesDefinition("B(OH)3", 0),
    AqueousSpeciesDefinition("B(OH)4-", -1),
    AqueousSpeciesDefinition("B3O3(OH)4-", -1),
    AqueousSpeciesDefinition("B4O5(OH)4-2", -2),
    AqueousSpeciesDefinition("CaB(OH)4+", 1),
    AqueousSpeciesDefinition("MgB(OH)4+", 1),
    AqueousSpeciesDefinition("H4SiO4", 0),
    AqueousSpeciesDefinition("H3SiO4-", -1),
    AqueousSpeciesDefinition("H2SiO4-2", -2),
)


MEAN_ELECTROLYTES: tuple[MeanElectrolyteDefinition, ...] = (
    MeanElectrolyteDefinition("NaCl", "NaCl", "Na+", "Cl-"),
    MeanElectrolyteDefinition("KCl", "KCl", "K+", "Cl-"),
    MeanElectrolyteDefinition("CaCl2", "CaCl₂", "Ca+2", "Cl-"),
    MeanElectrolyteDefinition("MgCl2", "MgCl₂", "Mg+2", "Cl-"),
    MeanElectrolyteDefinition("Na2SO4", "Na₂SO₄", "Na+", "SO4-2"),
    MeanElectrolyteDefinition("HBr", "HBr", "H+", "Br-"),
)
