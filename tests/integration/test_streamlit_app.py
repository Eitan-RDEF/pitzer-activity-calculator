import os
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PHREEQC_INTEGRATION") != "1",
    reason="Set RUN_PHREEQC_INTEGRATION=1 to run the Streamlit calculation smoke test.",
)


def test_default_nacl_workflow_renders_complete_results() -> None:
    app = AppTest.from_file(Path(__file__).parents[2] / "streamlit_app.py")
    app.run(timeout=20)

    assert not app.exception
    app.button[0].click().run(timeout=20)

    assert not app.exception
    assert len(app.metric) == 4
    assert len(app.dataframe) == 3
