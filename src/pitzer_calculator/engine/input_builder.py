"""Build deterministic PHREEQC input from validated domain objects."""

from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.domain.species import COMPONENT_BY_KEY, COMPONENTS


def build_phreeqc_input(solution: SolutionInput) -> str:
    """Return a PHREEQC input deck for the initial H+ activity calculation."""

    lines = [
        "SOLUTION 1",
        f"    temp {solution.temperature_c:.12g}",
        f"    pH {solution.ph:.12g}",
        "    units mol/kgw",
        "    -water 1.0",
    ]

    for component in COMPONENTS:
        value = solution.components_molal.get(component.key, 0.0)
        if value:
            lines.append(f"    {component.phreeqc_name} {value:.12g}")

    # Keep output headings stable: the engine adapter treats them as an API contract.
    lines.extend(
        [
            "",
            "SELECTED_OUTPUT",
            "    -reset false",
            "    -solution true",
            "    -pH true",
            "    -ionic_strength true",
            "    -percent_error true",
            "",
            "USER_PUNCH",
            "    -headings loga_H logm_H loggamma_H gamma_H mol_H act_H",
            '    10 PUNCH LA("H+")',
            '    20 PUNCH LM("H+")',
            '    30 PUNCH LA("H+") - LM("H+")',
            '    40 PUNCH 10^(LA("H+") - LM("H+"))',
            '    50 PUNCH MOL("H+")',
            '    60 PUNCH 10^LA("H+")',
            "",
            "END",
        ]
    )
    return "\n".join(lines) + "\n"


def phreeqc_name_for(key: str) -> str:
    """Expose the supported-component mapping for exports and diagnostics."""

    return COMPONENT_BY_KEY[key].phreeqc_name

