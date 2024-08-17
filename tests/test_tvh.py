import tsclean
from tsclean.config import getConfig
from tsclean.tvh import sendToTVH, getRadioRecorded


def test_sendToTVH():
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    data = {"limit": 100}
    j = sendToTVH("dvr/entry/grid_finished", data)
    assert "total" in j


def test_getRadioRecorded():
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    rrecs = getRadioRecorded()
    assert len(rrecs) == 0
