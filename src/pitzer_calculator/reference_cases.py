"""Typed access to the reviewed public reference-case library."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from pitzer_calculator.config import DATA_DIR

REFERENCE_LIBRARY_PATH = DATA_DIR / "examples" / "validation_library.json"

EVIDENCE_LABELS = {
    "experimental_or_evaluated_reference": "Independent experimental/evaluated reference",
    "software_benchmark": "Published software benchmark",
}


@dataclass(frozen=True, slots=True)
class ReferenceSource:
    """Citation and locator for one published reference case."""

    citation: str
    url: str
    locator: str
    local_document: str
    license_url: str | None = None


@dataclass(frozen=True, slots=True)
class ReferenceCase:
    """A reviewed composition and the source values available for consultation."""

    id: str
    title: str
    description: str
    evidence_type: str
    temperature_c: float
    pressure_atm: float
    known_ph: float
    components_molal: Mapping[str, float]
    published_outputs: Mapping[str, Any]
    source: ReferenceSource
    assumptions: tuple[str, ...]

    @property
    def evidence_label(self) -> str:
        """Return the public, scientifically explicit evidence-class label."""

        return EVIDENCE_LABELS[self.evidence_type]


@dataclass(frozen=True, slots=True)
class PublishedOutputRow:
    """One user-facing published result from a reference case."""

    property: str
    value: float
    unit: str
    expanded_uncertainty_95: float | None = None


def _parse_case(raw_case: Mapping[str, Any]) -> ReferenceCase:
    """Validate and convert one JSON case at the application-data boundary."""

    inputs = raw_case["input"]
    if inputs["composition_unit"] != "mol/kg_H2O":
        raise ValueError(
            f"Reference case {raw_case['id']} does not use the supported molality basis."
        )

    source = raw_case["source"]
    evidence_type = str(raw_case["evidence_type"])
    if evidence_type not in EVIDENCE_LABELS:
        raise ValueError(
            f"Reference case {raw_case['id']} has an unknown evidence type: {evidence_type}"
        )

    return ReferenceCase(
        id=str(raw_case["id"]),
        title=str(raw_case["title"]),
        description=str(raw_case["description"]),
        evidence_type=evidence_type,
        temperature_c=float(inputs["temperature_c"]),
        pressure_atm=float(inputs["pressure_atm"]),
        known_ph=float(inputs["known_ph"]),
        components_molal={
            str(component): float(value)
            for component, value in inputs["components"].items()
        },
        published_outputs=dict(raw_case["published_outputs"]),
        source=ReferenceSource(
            citation=str(source["citation"]),
            url=str(source["url"]),
            locator=str(source["locator"]),
            local_document=str(source["local_document"]),
            license_url=(str(source["license_url"]) if source.get("license_url") else None),
        ),
        assumptions=tuple(str(item) for item in raw_case["assumptions"]),
    )


@lru_cache(maxsize=1)
def load_reference_cases(path: Path = REFERENCE_LIBRARY_PATH) -> tuple[ReferenceCase, ...]:
    """Load the reviewed production library in its curated display order."""

    library = json.loads(path.read_text(encoding="utf-8"))
    cases = tuple(_parse_case(item) for item in library["cases"])
    if len({case.id for case in cases}) != len(cases):
        raise ValueError("Reference-case identifiers must be unique.")
    return cases


def published_output_rows(case: ReferenceCase) -> tuple[PublishedOutputRow, ...]:
    """Normalize the supported source-output shapes for compact UI rendering."""

    outputs = case.published_outputs
    rows: list[PublishedOutputRow] = []

    mean_coefficients = outputs.get("mean_activity_coefficients", {})
    mean_uncertainties = outputs.get(
        "mean_activity_coefficient_expanded_uncertainty_95", {}
    )
    for electrolyte, value in mean_coefficients.items():
        rows.append(
            PublishedOutputRow(
                property=f"Mean activity coefficient γ± ({electrolyte})",
                value=float(value),
                unit="dimensionless",
                expanded_uncertainty_95=(
                    float(mean_uncertainties[electrolyte])
                    if electrolyte in mean_uncertainties
                    else None
                ),
            )
        )

    scalar_outputs = (
        ("osmotic_coefficient", "Osmotic coefficient", "dimensionless"),
        ("water_activity", "Water activity", "dimensionless"),
        (
            "ionic_strength_mol_per_kg_H2O",
            "Ionic strength",
            "mol/kg H₂O",
        ),
    )
    for key, label, unit in scalar_outputs:
        if key in outputs:
            rows.append(
                PublishedOutputRow(
                    property=label,
                    value=float(outputs[key]),
                    unit=unit,
                )
            )

    for index, measurement in enumerate(
        outputs.get("osmotic_coefficient_measurements", []), start=1
    ):
        rows.append(
            PublishedOutputRow(
                property=f"Osmotic coefficient — measurement {index}",
                value=float(measurement["value"]),
                unit="dimensionless",
                expanded_uncertainty_95=float(measurement["expanded_uncertainty_95"]),
            )
        )

    return tuple(rows)
