import os

from tsclean.filename import splitFqfn


def test_splitFqfn():
    home = os.path.expanduser("~/")
    fqfn = os.path.abspath("tests/The-News-Quiz-E08.ts")
    fdir, bfn, ext = splitFqfn(fqfn)
    assert fdir == f"{home}src/tsclean/tests"
    assert bfn == "The-News-Quiz-E08"
    assert ext == ".ts"
