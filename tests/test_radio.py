import os

import tsclean
from tsclean.radio import copyRadioFile


def test_copyRadioFile():
    show = {"filename": "/var/lib/tvheadend/radio/The Wilsons Save The World-1.ts"}
    tsclean.radiooutputdir = "/tmp"
    copyRadioFile(show)
    oppath = os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))
    fn = show["filename"]
    basefn = fn.split("/")[-1]
    dest = f"{oppath}/{basefn}"
    assert os.path.exists(dest)
