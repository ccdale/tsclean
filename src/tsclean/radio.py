import os
import sys

from fabric import Connection

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.shell import listCmd, shellCommand


def copyRadioFile(show):
    try:
        fn = show["filename"]
        basefn = fn.split("/")[-1]
        oppath = os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))
        # print(f"{oppath=}")
        os.makedirs(oppath, exist_ok=True)
        dest = f"{oppath}/{basefn}"
        # print(f"{dest=}")
        with Connection(host=tsclean.sshhost, user=tsclean.sshuser) as c:
            c.get(show["filename"], dest)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
