import os

from tsclean.filename import splitFqfn


def test_splitFqfn():
    home = os.path.expanduser("~/")
    fqfn = os.path.abspath(f"tests/data/radio.ts")
    fdir, bfn, ext = splitFqfn(fqfn)
    assert fdir == f"{home}src/tsclean/tests/data"
    assert bfn == "radio"
    assert ext == ".ts"
