import tsclean
from tsclean.config import getConfig
from tsclean.tvh import sendToTVH


def test_sendToTVH():
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    data = {"limit": 100}
    j = sendToTVH("dvr/entry/grid_finished", data)
    assert "total" in j
