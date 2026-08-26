"""Supported component metadata for the first calculator release."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ComponentDefinition:
    key: str
    label: str
    phreeqc_name: str
    group: str


COMPONENTS: tuple[ComponentDefinition, ...] = (
    ComponentDefinition("Na", "Na⁺", "Na", "Cations"),
    ComponentDefinition("K", "K⁺", "K", "Cations"),
    ComponentDefinition("Li", "Li⁺", "Li", "Cations"),
    ComponentDefinition("Ca", "Ca²⁺", "Ca", "Cations"),
    ComponentDefinition("Mg", "Mg²⁺", "Mg", "Cations"),
    ComponentDefinition("Sr", "Sr²⁺", "Sr", "Cations"),
    ComponentDefinition("Ba", "Ba²⁺", "Ba", "Cations"),
    ComponentDefinition("Fe2", "Fe²⁺", "Fe(2)", "Cations"),
    ComponentDefinition("Fe3", "Fe³⁺", "Fe(3)", "Cations"),
    ComponentDefinition("Al", "Al³⁺", "Al", "Cations"),
    ComponentDefinition("Cl", "Cl⁻", "Cl", "Anions and totals"),
    ComponentDefinition("Br", "Br⁻", "Br", "Anions and totals"),
    ComponentDefinition("SO4", "Total S(VI)", "S(6)", "Anions and totals"),
    ComponentDefinition("C4", "Total inorganic C(IV)", "C(4)", "Anions and totals"),
)

COMPONENT_BY_KEY = {component.key: component for component in COMPONENTS}

