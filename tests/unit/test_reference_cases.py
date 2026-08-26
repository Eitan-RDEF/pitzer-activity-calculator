from pitzer_calculator.reference_cases import (
    load_reference_cases,
    published_output_rows,
)


def test_reviewed_reference_library_loads_all_public_cases() -> None:
    cases = load_reference_cases()

    assert len(cases) == 30
    assert len({case.id for case in cases}) == 30
    assert {case.evidence_label for case in cases} == {
        "Independent experimental/evaluated reference",
        "Published software benchmark",
    }


def test_mean_coefficient_reference_is_normalized_with_source_uncertainty() -> None:
    case = next(
        item
        for item in load_reference_cases()
        if item.id == "nist_thermoml_2012_cacl2_0p5m_25c"
    )

    assert case.components_molal == {"Ca": 0.5, "Cl": 1.0}
    assert case.known_ph == 7.0
    rows = published_output_rows(case)
    assert len(rows) == 1
    row = rows[0]
    assert row.property == "Mean activity coefficient γ± (CaCl2)"
    assert row.value == 0.449
    assert row.expanded_uncertainty_95 == 0.001
    assert row.unit == "dimensionless"


def test_repeated_osmotic_measurements_remain_separate_rows() -> None:
    case = next(
        item
        for item in load_reference_cases()
        if item.id == "nist_thermoml_2014_na2so4_0p5m_25c"
    )

    rows = published_output_rows(case)
    assert [row.value for row in rows] == [0.717, 0.69]
    assert [row.expanded_uncertainty_95 for row in rows] == [0.014, 0.015]
    assert [row.property for row in rows] == [
        "Osmotic coefficient — measurement 1",
        "Osmotic coefficient — measurement 2",
    ]
