from pathlib import Path

import tomllib

from pitzer_calculator import __version__

ROOT = Path(__file__).parents[2]


def test_release_version_is_consistent() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert metadata["project"]["version"] == "1.0.0"
    assert __version__ == metadata["project"]["version"]
    assert metadata["project"]["license"] == "MIT"
    assert metadata["project"]["urls"]["Homepage"] == (
        "https://pitzer-calculator.streamlit.app"
    )
    assert not any(
        classifier.startswith("License ::")
        for classifier in metadata["project"]["classifiers"]
    )


def test_public_release_documents_exist() -> None:
    for relative_path in (
        "LICENSE",
        "PRIVACY.md",
        "CONTACT.md",
        "SECURITY.md",
        "docs/third-party-notices.md",
    ):
        assert (ROOT / relative_path).is_file(), relative_path
