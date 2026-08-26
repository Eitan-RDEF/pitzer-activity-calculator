from pathlib import Path

from pitzer_calculator.domain.species import COMPONENTS
from scripts.audit_pitzer_database import audit_database

DATABASE_PATH = Path("data/databases/pitzer.dat")
EXPECTED_SHA256 = "3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb"


def test_database_provenance_and_inventory_are_stable() -> None:
    inventory = audit_database(DATABASE_PATH)

    assert inventory.sha256 == EXPECTED_SHA256
    assert inventory.byte_length == 37_225
    assert inventory.encoding == "cp1252"
    assert len(inventory.master_components) == 28
    assert len(inventory.parameter_entries) == 268
    assert len(inventory.mean_gammas) == 21


def test_database_does_not_define_al_or_iron_redox_states() -> None:
    inventory = audit_database(DATABASE_PATH)
    names = {component.name for component in inventory.master_components}

    assert "Fe" in names
    assert "Al" not in names
    assert "Fe(2)" not in names
    assert "Fe(3)" not in names


def test_iron_master_species_is_ferrous_iron() -> None:
    inventory = audit_database(DATABASE_PATH)
    components = {
        component.name: component.master_species for component in inventory.master_components
    }

    assert components["Fe"] == "Fe+2"


def test_every_exposed_component_exists_in_database_master_components() -> None:
    inventory = audit_database(DATABASE_PATH)
    database_names = {component.name for component in inventory.master_components}

    assert {component.phreeqc_name for component in COMPONENTS} <= database_names


def test_expected_parameter_block_counts() -> None:
    inventory = audit_database(DATABASE_PATH)
    counts = {
        block: sum(entry.block == block for entry in inventory.parameter_entries)
        for block in ("B0", "B1", "B2", "C0", "THETA", "LAMBDA", "ZETA", "PSI")
    }

    assert counts == {
        "B0": 54,
        "B1": 48,
        "B2": 8,
        "C0": 32,
        "THETA": 30,
        "LAMBDA": 27,
        "ZETA": 10,
        "PSI": 59,
    }
