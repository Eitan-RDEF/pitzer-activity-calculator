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
    # pitzer.dat defines the master component as "Fe" with Fe+2 as its master
    # species. It contains no iron redox couple, so this input is fixed Fe(II).
    ComponentDefinition("Fe2", "Fe(II) total", "Fe", "Cations"),
    ComponentDefinition("Cl", "Cl⁻", "Cl", "Anions and totals"),
    ComponentDefinition("Br", "Br⁻", "Br", "Anions and totals"),
    ComponentDefinition("SO4", "Total S(VI)", "S(6)", "Anions and totals"),
    ComponentDefinition("C4", "Total inorganic C(IV)", "C(4)", "Anions and totals"),
)

COMPONENT_BY_KEY = {component.key: component for component in COMPONENTS}
