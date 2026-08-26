from pitzer_calculator.domain.models import SolutionInput
from pitzer_calculator.engine.input_builder import build_phreeqc_input


def test_builds_deterministic_solution_and_selected_output() -> None:
    text = build_phreeqc_input(
        SolutionInput(
            ph=6.5,
            temperature_c=40.0,
            components_molal={"Na": 1.0, "Cl": 1.0, "SO4": 0.0},
        )
    )

    assert "    temp 40" in text
    assert "    pH 6.5" in text
    assert "    Na 1" in text
    assert "    Cl 1" in text
    assert "    S(6)" not in text
    assert "    -percent_error true" in text
    assert '-headings loga_H logm_H loggamma_H gamma_H mol_H act_H' in text


def test_uses_valence_specific_phreeqc_names() -> None:
    text = build_phreeqc_input(
        SolutionInput(
            ph=7.0,
            temperature_c=25.0,
            components_molal={"Fe2": 0.01, "Fe3": 0.02, "C4": 0.03},
        )
    )

    assert "    Fe(2) 0.01" in text
    assert "    Fe(3) 0.02" in text
    assert "    C(4) 0.03" in text

