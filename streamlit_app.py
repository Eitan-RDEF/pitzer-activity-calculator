"""Streamlit Community Cloud entry point."""

import streamlit as st

from pitzer_calculator.ui.main import render_app

st.set_page_config(
    page_title="Pitzer Activity Calculator",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_app()

