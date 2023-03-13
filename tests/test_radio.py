import os

import tsclean
from tsclean.config import getConfig
from tsclean.radio import copyRadioFile
from tsclean.tvh import getRadioRecorded


def test_copyRadioFile():
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    tsclean.sshuser = cfg.get("sshuser", "")
    tsclean.sshhost = cfg.get("sshhost", "")
    rrecs = getRadioRecorded()
    show = rrecs[0]
    tsclean.radiooutputdir = "/tmp"
    copyRadioFile(show)
    oppath = os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))
    fn = show["filename"]
    basefn = fn.split("/")[-1]
    dest = f"{oppath}/{basefn}"
    assert os.path.exists(dest)
    os.unlink(dest)
    assert not os.path.exists(dest)
