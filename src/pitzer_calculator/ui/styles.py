"""Load the small amount of project-owned visual styling."""

import streamlit as st

from pitzer_calculator.config import ASSETS_DIR


def apply_styles() -> None:
    css_path = ASSETS_DIR / "styles.css"
    if css_path.is_file():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
