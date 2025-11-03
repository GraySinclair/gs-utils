import importlib.util
import pytest

FABRIC = importlib.util.find_spec("notebookutils") is not None

@pytest.mark.skipif(not FABRIC, reason="Fabric-only test")
def test_setup_smoke():
    from gs_utils import setup
    ctx = setup(require_spark=False)
    assert ctx.logger is not None
