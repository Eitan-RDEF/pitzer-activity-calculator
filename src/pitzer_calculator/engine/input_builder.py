"""Build deterministic PHREEQC input from validated domain objects."""

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.domain.species import (
    AQUEOUS_SPECIES,
    COMPONENT_BY_KEY,
    COMPONENTS,
    MEAN_ELECTROLYTES,
)


def species_column(index: int, quantity: str) -> str:
    """Return a stable selected-output heading for one species quantity."""

    return f"sp_{index:02d}_{quantity}"


def mean_gamma_column(key: str) -> str:
    return f"mean_{key.lower()}"


def build_phreeqc_input(solution: SolutionInput) -> str:
    """Return the complete known-pH, closed-system PHREEQC input deck."""

    lines = [
        "PITZER",
        "    -macinnes true",
        "    -use_etheta true",
        "    -redox false",
        "",
        "SOLUTION 1 Known-pH closed system",
        f"    temp {solution.temperature_c:.12g}",
        f"    pressure {solution.pressure_atm:.12g}",
        f"    pH {solution.ph:.12g}",
        "    units mol/kgw",
        "    -water 1.0",
    ]

    for component in COMPONENTS:
        value = solution.components_molal.get(component.key, 0.0)
        if value:
            lines.append(f"    {component.phreeqc_name} {value:.12g}")

    lines.extend(
        [
            "",
            "SELECTED_OUTPUT 1",
            "    -reset false",
            "    -solution true",
            "    -pH true",
            "    -temperature true",
            "    -alkalinity true",
            "    -ionic_strength true",
            "    -water true",
            "    -charge_balance true",
            "    -percent_error true",
            "",
            "USER_PUNCH 1",
        ]
    )

    headings = ["water_activity", "osmotic_coefficient", "pressure_atm"]
    for index, _species in enumerate(AQUEOUS_SPECIES):
        headings.extend(
            species_column(index, quantity)
            for quantity in ("m", "a", "gamma", "lm", "la", "lg")
        )
    headings.extend(mean_gamma_column(item.key) for item in MEAN_ELECTROLYTES)
    lines.append(f"    -headings {' '.join(headings)}")

    line_number = 10
    lines.append(f'    {line_number} PUNCH ACT("H2O"), OSMOTIC, PRESSURE')
    for species in AQUEOUS_SPECIES:
        line_number += 10
        name = species.name
        lines.append(
            f'    {line_number} PUNCH MOL("{name}"), ACT("{name}"), '
            f'GAMMA("{name}"), LM("{name}"), LA("{name}"), LG("{name}")'
        )
    for electrolyte in MEAN_ELECTROLYTES:
        line_number += 10
        lines.append(f'    {line_number} PUNCH MEANG("{electrolyte.key}")')

    lines.extend(["", "END"])
    return "\n".join(lines) + "\n"


def phreeqc_name_for(key: str) -> str:
    """Expose the supported-component mapping for exports and diagnostics."""

    return COMPONENT_BY_KEY[key].phreeqc_name

