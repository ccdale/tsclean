import os
import sys

from tsclean import errorExit, errorNotify, errorRaise


def splitFqfn(fqfn):
    try:
        fdir, fn = os.path.split(fqfn)
        bfn, ext = os.path.splitext(fn)
        return fdir, bfn, ext
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
