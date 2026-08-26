"""Application paths and stable project metadata."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "databases" / "pitzer.dat"
ASSETS_DIR = PROJECT_ROOT / "assets"

APP_NAME = "Pitzer Activity Calculator"
APP_TAGLINE = "High-ionic-strength aqueous calculations without the PHREEQC learning curve."

