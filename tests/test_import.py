"""Test sankey-streamlit."""

import sankey_streamlit


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(sankey_streamlit.__name__, str)
