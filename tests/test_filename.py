import os

from tsclean.filename import incrementFileName, splitFqfn


def test_splitFqfn():
    home = os.path.expanduser("~/")
    fqfn = os.path.abspath(f"tests/data/radio.ts")
    fdir, bfn, ext = splitFqfn(fqfn)
    assert fdir == f"{home}src/tsclean/tests/data"
    assert bfn == "radio"
    assert ext == ".ts"


def test_incrementFileName():
    fqfn = "/home/wibble/somedir/filename_014.ext"
    ifqfn = incrementFileName(fqfn)
    assert ifqfn == "/home/wibble/somedir/filename_015.ext"


def test_incrementFileName_no_number():
    fqfn = "/home/wibble/somedir/filename.ext"
    ifqfn = incrementFileName(fqfn)
    assert ifqfn == fqfn


def test_incrementFileName_number_not_at_end():
    fqfn = "/home/wibble/somedir/filen_002ame.ext"
    ifqfn = incrementFileName(fqfn)
    assert ifqfn == fqfn


def test_incrementFileName_large_number():
    fqfn = "/home/wibble/somedir/filename_999.ext"
    ifqfn = incrementFileName(fqfn)
    assert ifqfn == "/home/wibble/somedir/filename_1000.ext"


def test_incrementFileName_addnumber():
    fqfn = "/home/wibble/somedir/filename.ext"
    expected = "/home/wibble/somedir/filename_000.ext"
    ifqfn = incrementFileName(fqfn, addnumber=True)
    assert ifqfn == expected
