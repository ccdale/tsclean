from tsclean.config import getConfig


def test_getConfig():
    cfg = getConfig()
    assert cfg.get("tvhipaddr", "notset") != "notset"
    assert cfg.get("tvhipaddr", "notset") == "druidmedia:9981"
