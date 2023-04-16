import os
import re
import sys

from tsclean import errorExit, errorNotify, errorRaise


def splitFqfn(fqfn):
    try:
        fdir, fn = os.path.split(fqfn)
        bfn, ext = os.path.splitext(fn)
        return fdir, bfn, ext
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def incrementFileName(fqfn, addnumber=False):
    try:
        fdir, bfn, ext = splitFqfn(fqfn)
        match = re.search("_[0-9]+$", bfn)
        if match:
            scn = match[0][1:]
            nextcn = int(scn) + 1
            nscn = f"{nextcn:0>{len(scn)}}"
            bfn = bfn.replace(match[0], f"_{nscn}")
        elif addnumber:
            bfn = f"{bfn}_000"
        return "/".join([fdir, f"{bfn}{ext}"])
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
