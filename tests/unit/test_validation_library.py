import json
from pathlib import Path
from typing import Any

from pitzer_calculator.domain.species import COMPONENTS, MEAN_ELECTROLYTES

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LIBRARY_PATH = REPOSITORY_ROOT / "data" / "examples" / "validation_library.json"


def _library() -> dict[str, Any]:
    return json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _all_keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _all_keys(child)}
    return set()


def test_library_contains_usgs_benchmarks_and_thermoml_references() -> None:
    library = _library()

    assert library["schema_version"] == "1.0.0"
    assert len(library["cases"]) == 30
    assert len({case["id"] for case in library["cases"]}) == 30
    assert {case["evidence_type"] for case in library["cases"]} == {
        "experimental_or_evaluated_reference",
        "software_benchmark",
    }


def test_thermoml_grid_has_two_salts_concentrations_and_four_temperatures() -> None:
    cases = [
        case
        for case in _library()["cases"]
        if case["id"].startswith("nist_thermoml_2016_")
    ]

    assert len(cases) == 16
    assert {case["input"]["temperature_c"] for case in cases} == {0.0, 20.0, 50.0, 70.0}
    assert {
        next(iter(case["published_outputs"]["mean_activity_coefficients"]))
        for case in cases
    } == {"KCl", "NaCl"}
    assert {
        next(iter(case["input"]["components"].values())) for case in cases
    } == {0.1, 0.5}


def test_thermoml_values_match_the_archived_machine_readable_source() -> None:
    library = _library()
    source_path = (
        REPOSITORY_ROOT
        / "docs"
        / "references"
        / "validation"
        / "nist-thermoml-partanen-2016-nacl-kcl.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_datasets = {
        "KCl": source["PureOrMixtureData"][0],
        "NaCl": source["PureOrMixtureData"][1],
    }

    for case in library["cases"]:
        if not case["id"].startswith("nist_thermoml_2016_"):
            continue

        published = case["published_outputs"]
        electrolyte = next(iter(published["mean_activity_coefficients"]))
        temperature_k = case["input"]["temperature_c"] + 273.15
        molality = case["input"]["components"]["K" if electrolyte == "KCl" else "Na"]
        source_row = next(
            row
            for row in source_datasets[electrolyte]["NumValues"]
            if row["VariableValue"][0]["nVarValue"] == temperature_k
            and row["VariableValue"][1]["nVarValue"] == molality
        )

        assert published["mean_activity_coefficients"][electrolyte] == source_row[
            "PropertyValue"
        ][0]["nPropValue"]
        assert published["mean_activity_coefficient_expanded_uncertainty_95"][
            electrolyte
        ] == source_row["PropertyValue"][0]["CombinedUncertainty"][
            "nCombExpandUncertValue"
        ]


def test_divalent_chloride_grid_uses_exact_source_molalities_and_stoichiometry() -> None:
    cases = [
        case
        for case in _library()["cases"]
        if case["id"].startswith(
            ("nist_thermoml_2012_cacl2_", "nist_thermoml_2015_mgcl2_")
        )
    ]

    assert len(cases) == 8
    assert {case["input"]["temperature_c"] for case in cases} == {25.0}

    molalities: dict[str, set[float]] = {"CaCl2": set(), "MgCl2": set()}
    cations = {"CaCl2": "Ca", "MgCl2": "Mg"}
    for case in cases:
        electrolyte = next(
            iter(case["published_outputs"]["mean_activity_coefficients"])
        )
        cation_molality = case["input"]["components"][cations[electrolyte]]
        assert case["input"]["components"]["Cl"] == 2 * cation_molality
        molalities[electrolyte].add(cation_molality)

    assert molalities == {
        "CaCl2": {0.1, 0.5, 1.0, 3.0},
        "MgCl2": {0.0833, 0.3333, 1.0, 2.0},
    }


def test_divalent_chloride_values_match_archived_thermoml_sources() -> None:
    source_specs = {
        "CaCl2": {
            "path": "nist-thermoml-partanen-2012-cacl2.json",
            "dataset": 0,
            "id_prefix": "nist_thermoml_2012_cacl2_",
            "cation": "Ca",
        },
        "MgCl2": {
            "path": "nist-thermoml-rouhi-bagherinia-2015-mgcl2.json",
            "dataset": 1,
            "id_prefix": "nist_thermoml_2015_mgcl2_",
            "cation": "Mg",
        },
    }
    source_directory = REPOSITORY_ROOT / "docs" / "references" / "validation"

    for electrolyte, spec in source_specs.items():
        source = json.loads(
            (source_directory / spec["path"]).read_text(encoding="utf-8")
        )
        dataset = source["PureOrMixtureData"][spec["dataset"]]
        cases = [
            case
            for case in _library()["cases"]
            if case["id"].startswith(spec["id_prefix"])
        ]

        for case in cases:
            molality = case["input"]["components"][spec["cation"]]
            source_row = next(
                row
                for row in dataset["NumValues"]
                if row["VariableValue"][0]["nVarValue"] == molality
            )
            published = case["published_outputs"]
            property_value = source_row["PropertyValue"][0]

            assert published["mean_activity_coefficients"][electrolyte] == property_value[
                "nPropValue"
            ]
            assert published["mean_activity_coefficient_expanded_uncertainty_95"][
                electrolyte
            ] == property_value["CombinedUncertainty"]["nCombExpandUncertValue"]


def test_na2so4_cases_preserve_source_replicates_and_stoichiometry() -> None:
    source_path = (
        REPOSITORY_ROOT
        / "docs"
        / "references"
        / "validation"
        / "nist-thermoml-held-2014-na2so4.json"
    )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    dataset = next(
        item
        for item in source["PureOrMixtureData"]
        if item["nPureOrMixtureDataNumber"] == 81
    )
    cases = [
        case
        for case in _library()["cases"]
        if case["id"].startswith("nist_thermoml_2014_na2so4_")
    ]

    assert len(cases) == 2
    assert {case["input"]["components"]["SO4"] for case in cases} == {0.5, 1.0}

    for case in cases:
        molality = case["input"]["components"]["SO4"]
        assert case["input"]["components"]["Na"] == 2 * molality

        source_rows = [
            row
            for row in dataset["NumValues"]
            if row["VariableValue"][0]["nVarValue"] == molality
        ]
        source_measurements = [
            {
                "value": row["PropertyValue"][0]["nPropValue"],
                "expanded_uncertainty_95": row["PropertyValue"][0][
                    "CombinedUncertainty"
                ]["nCombExpandUncertValue"],
            }
            for row in source_rows
        ]

        assert case["published_outputs"]["osmotic_coefficient_measurements"] == (
            source_measurements
        )


def test_library_uses_only_supported_component_and_electrolyte_keys() -> None:
    library = _library()
    component_keys = {component.key for component in COMPONENTS}
    electrolyte_keys = {electrolyte.key for electrolyte in MEAN_ELECTROLYTES}

    for case in library["cases"]:
        inputs = case["input"]
        assert inputs["composition_unit"] == "mol/kg_H2O"
        assert set(inputs["components"]) <= component_keys
        assert all(value >= 0 for value in inputs["components"].values())
        assert set(
            case["published_outputs"].get("mean_activity_coefficients", {})
        ) <= electrolyte_keys


def test_library_conditions_fit_the_current_app_boundary() -> None:
    for case in _library()["cases"]:
        inputs = case["input"]
        assert 0 <= inputs["temperature_c"] <= 100
        assert inputs["pressure_atm"] == 1.0
        assert 0 <= inputs["known_ph"] <= 14


def test_library_sources_are_complete_and_local_documents_exist() -> None:
    for case in _library()["cases"]:
        source = case["source"]
        assert source["citation"]
        assert source["url"].startswith("https://")
        assert source["locator"]
        assert (REPOSITORY_ROOT / source["local_document"]).is_file()
        if "thermoml" in case["id"]:
            assert source["license_url"] == "https://www.nist.gov/open/license"


def test_public_library_contains_no_comparison_or_review_fields() -> None:
    forbidden = {
        "app_minus_reference",
        "app_results",
        "comparison_tolerance",
        "difference",
        "pass",
        "release_eligible",
        "reproduction",
        "status",
        "tolerance",
    }

    assert not (_all_keys(_library()) & forbidden)
