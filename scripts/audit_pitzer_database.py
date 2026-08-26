"""Inventory the bundled PHREEQC Pitzer database without modifying it.

The official file is Windows-1252 encoded. Preserving its bytes is important because the
repository records and verifies its upstream SHA-256 checksum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PARAMETER_ARITY = {
    "B0": 2,
    "B1": 2,
    "B2": 2,
    "C0": 2,
    "THETA": 2,
    "LAMBDA": 2,
    "ZETA": 3,
    "PSI": 3,
}


@dataclass(frozen=True, slots=True)
class MasterComponent:
    """One `SOLUTION_MASTER_SPECIES` entry and its source line."""

    name: str
    master_species: str
    line: int


@dataclass(frozen=True, slots=True)
class ParameterEntry:
    """One parsed Pitzer interaction entry with its coefficient series."""

    block: str
    species: tuple[str, ...]
    coefficients: tuple[float, ...]
    line: int

    @property
    def is_temperature_dependent(self) -> bool:
        """Return whether any coefficient beyond the constant term is active."""

        return len(self.coefficients) > 1 and any(value != 0 for value in self.coefficients[1:])


@dataclass(frozen=True, slots=True)
class MeanGammaDefinition:
    """One database-defined stoichiometric mean activity coefficient."""

    name: str
    cation: str
    cation_stoichiometry: int
    anion: str
    anion_stoichiometry: int
    line: int


@dataclass(frozen=True, slots=True)
class DatabaseInventory:
    """Reproducible provenance and parsed scientific inventory for `pitzer.dat`."""

    path: str
    byte_length: int
    sha256: str
    encoding: str
    master_components: tuple[MasterComponent, ...]
    parameter_entries: tuple[ParameterEntry, ...]
    mean_gammas: tuple[MeanGammaDefinition, ...]

    def as_dict(self) -> dict[str, Any]:
        """Return the stable JSON-serializable audit schema."""

        parameter_counts: dict[str, dict[str, int]] = {}
        for block in PARAMETER_ARITY:
            entries = [entry for entry in self.parameter_entries if entry.block == block]
            temperature_dependent = sum(entry.is_temperature_dependent for entry in entries)
            parameter_counts[block] = {
                "total": len(entries),
                "constant": len(entries) - temperature_dependent,
                "temperature_dependent": temperature_dependent,
            }

        species_blocks: dict[str, set[str]] = defaultdict(set)
        for entry in self.parameter_entries:
            for species in entry.species:
                species_blocks[species].add(entry.block)

        return {
            "path": self.path,
            "byte_length": self.byte_length,
            "sha256": self.sha256,
            "encoding": self.encoding,
            "master_components": [asdict(component) for component in self.master_components],
            "parameter_counts": parameter_counts,
            "parameter_species": {
                species: sorted(blocks) for species, blocks in sorted(species_blocks.items())
            },
            "parameter_entries": [asdict(entry) for entry in self.parameter_entries],
            "mean_gammas": [asdict(definition) for definition in self.mean_gammas],
        }


def _data_lines(lines: list[str], start_header: str, end_header: str) -> list[tuple[int, str]]:
    """Return uncommented data lines between two PHREEQC section headers."""

    collecting = False
    result: list[tuple[int, str]] = []
    for line_number, raw in enumerate(lines, 1):
        text = raw.split("#", 1)[0].strip()
        if text == start_header:
            collecting = True
            continue
        if collecting and text == end_header:
            break
        if collecting and text:
            result.append((line_number, text))
    return result


def parse_master_components(lines: list[str]) -> tuple[MasterComponent, ...]:
    """Parse analytical components from `SOLUTION_MASTER_SPECIES`."""

    components = []
    for line_number, text in _data_lines(
        lines, "SOLUTION_MASTER_SPECIES", "SOLUTION_SPECIES"
    ):
        tokens = text.split()
        if len(tokens) >= 2:
            components.append(MasterComponent(tokens[0], tokens[1], line_number))
    return tuple(components)


def parse_parameter_entries(lines: list[str]) -> tuple[ParameterEntry, ...]:
    """Parse supported interaction blocks from the database's `PITZER` section."""

    entries: list[ParameterEntry] = []
    block: str | None = None
    in_pitzer = False

    for line_number, raw in enumerate(lines, 1):
        text = raw.split("#", 1)[0].strip()
        if text == "PITZER":
            in_pitzer = True
            continue
        if not in_pitzer or not text:
            continue
        if text in {"GAS_BINARY_PARAMETERS", "EXCHANGE_MASTER_SPECIES"}:
            break
        if text.startswith("-"):
            candidate = text[1:].split()[0].upper()
            block = candidate if candidate in PARAMETER_ARITY else None
            continue
        if block is None:
            continue

        tokens = text.split()
        arity = PARAMETER_ARITY[block]
        if len(tokens) <= arity:
            continue
        entries.append(
            ParameterEntry(
                block=block,
                species=tuple(tokens[:arity]),
                coefficients=tuple(float(value) for value in tokens[arity:]),
                line=line_number,
            )
        )
    return tuple(entries)


def parse_mean_gammas(lines: list[str]) -> tuple[MeanGammaDefinition, ...]:
    """Parse curated electrolyte definitions from `MEAN_GAMMAS`."""

    definitions = []
    for line_number, text in _data_lines(lines, "MEAN_GAMMAS", "END"):
        tokens = text.split()
        if len(tokens) != 5:
            continue
        definitions.append(
            MeanGammaDefinition(
                name=tokens[0],
                cation=tokens[1],
                cation_stoichiometry=int(tokens[2]),
                anion=tokens[3],
                anion_stoichiometry=int(tokens[4]),
                line=line_number,
            )
        )
    return tuple(definitions)


def audit_database(path: Path) -> DatabaseInventory:
    """Read the database without altering its bytes and build a typed inventory."""

    raw = path.read_bytes()
    encoding = "cp1252"
    lines = raw.decode(encoding).splitlines()
    return DatabaseInventory(
        path=path.as_posix(),
        byte_length=len(raw),
        sha256=hashlib.sha256(raw).hexdigest(),
        encoding=encoding,
        master_components=parse_master_components(lines),
        parameter_entries=parse_parameter_entries(lines),
        mean_gammas=parse_mean_gammas(lines),
    )


def _human_summary(inventory: DatabaseInventory) -> str:
    """Render a compact terminal summary of an inventory."""

    data = inventory.as_dict()
    lines = [
        f"Database: {data['path']}",
        f"Bytes: {data['byte_length']}",
        f"SHA-256: {data['sha256']}",
        f"Encoding: {data['encoding']}",
        f"Master components: {len(data['master_components'])}",
        "Pitzer parameter blocks:",
    ]
    for block, counts in data["parameter_counts"].items():
        lines.append(
            f"  {block}: {counts['total']} total, "
            f"{counts['temperature_dependent']} temperature-dependent"
        )
    lines.append(f"Mean-gamma definitions: {len(data['mean_gammas'])}")
    return "\n".join(lines)


def main() -> None:
    """Run the read-only database audit command-line interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="Path to pitzer.dat")
    parser.add_argument("--json", action="store_true", help="Print the full inventory as JSON")
    args = parser.parse_args()

    inventory = audit_database(args.database)
    if args.json:
        print(json.dumps(inventory.as_dict(), indent=2))
    else:
        print(_human_summary(inventory))


if __name__ == "__main__":
    main()
