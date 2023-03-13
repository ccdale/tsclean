import os
import re
import sys

from fabric import Connection
from mutagen.easyid3 import EasyID3

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.ffmpeg import makeAudioFile
from tsclean.tvh import deleteShow

# TODO
# DONE - Copy file from druidmedia
# DONE - convert file to mp3
# DONE - tag file with show information
# DONE - move file into the radio directory hierarchy


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


def doRadio(show, testing=True):
    try:
        src = copyRadioFile(show)
        fn = show["filename"]
        basefn = fn.split("/")[-1].split(".")[0]
        dest = "/".join([os.path.dirname(src), f"{basefn}.mp3"])
        mp3 = makeAudioFile(src, dest)
        if mp3 is None:
            raise Exception(f"failed to create mp3 from {src}")
        os.unlink(src)
        if not testing:
            deleteShow(show)
        audio = EasyID3(mp3)
        audio["genre"] = "Speech"
        audio["title"] = show["disp_title"]
        # audio["comment"] = show["disp_description"]
        # audio["album"] = show["disp_title"]
        audio["albumartist"] = show["channelname"]
        # match = re.search("[0-9]+", show["disp_description"])
        # if match:
        #     audio["track"] = match[0]
        audio.save()
        if not testing:
            destdir = (
                f"{tsclean.radiooutputdir}/{show['channelname']}/{show['disp_title']}"
            )
            os.makedirs(destdir)
            dest = "/".join([destdir, os.path.basename(mp3)])
            os.rename(mp3, dest)
        return dest
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
