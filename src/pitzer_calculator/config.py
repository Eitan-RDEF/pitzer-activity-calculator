"""Application paths and stable project metadata."""

import os
from pathlib import Path

# Installed containers keep runtime data outside the Python package. Local source checkouts
# need no environment variable because the repository root is derivable from this file.
PROJECT_ROOT = Path(
    os.environ.get("PITZER_PROJECT_ROOT", Path(__file__).resolve().parents[2])
).resolve()
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "databases" / "pitzer.dat"
ASSETS_DIR = PROJECT_ROOT / "assets"

APP_NAME = "Pitzer Activity Calculator"
APP_TAGLINE = "High-ionic-strength aqueous calculations without the PHREEQC learning curve."
