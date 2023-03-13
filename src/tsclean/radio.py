import os
import sys

from fabric import Connection

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.ffmpeg import makeAudioFile

# TODO
# DONE - Copy file from druidmedia
# convert file to mp3
# tag file with show information
# move file into the radio directory hierarchy


def copyRadioFile(show):
    try:
        fn = show["filename"]
        basefn = fn.split("/")[-1]
        oppath = os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))
        os.makedirs(oppath, exist_ok=True)
        dest = f"{oppath}/{basefn}"
        with Connection(host=tsclean.sshhost, user=tsclean.sshuser) as c:
            c.get(show["filename"], dest)
        return dest
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def doRadio(show):
    try:
        src = copyRadioFile(show)
        fn = show["filename"]
        basefn = fn.split("/")[-1].split(".")[0]
        dest = "/".join([os.path.dirname(src), basefn, ".mp3"])
        mp3 = makeAudioFile(src, dest)
        if mp3 is None:
            raise Exception(f"failed to create mp3 from {src}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
