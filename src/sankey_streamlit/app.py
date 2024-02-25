"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"sankey-streamlit v{version('sankey-streamlit')}")  # type: ignore[no-untyped-call]
