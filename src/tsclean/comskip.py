import sys

from tsclean import errorExit, errorNotify, errorRaise
from tsclean.shell import beNice, shellCommand


def doComSkip(fqfn):
    try:
        cmd = ["comskip", "-t", "-d", "255", fqfn]
        ccmd = beNice(cmd)
        _, _ = shellCommand(ccmd, canfail=True)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)