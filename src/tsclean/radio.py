import os
import re
import sys

from fabric import Connection
from mutagen.easyid3 import EasyID3

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.ffmpeg import makeAudioFile
from tsclean.filename import incrementFileName
from tsclean.tvh import deleteShow

# TODO
# DONE - Copy file from druidmedia
# DONE - convert file to mp3
# DONE - tag file with show information
# DONE - move file into the radio directory hierarchy


def copyRadioFile(show):
    """copy a radio show file from the tvheadend directory.

    var testing: the filename of a test file, will skip this step if file exists
    """
    try:
        fn = show["filename"]
        basefn = os.path.basename(fn)
        # basefn = fn.split("/")[-1]
        oppath = os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))
        os.makedirs(oppath, exist_ok=True)
        dest = f"{oppath}/{basefn}"
        with Connection(host=tsclean.sshhost, user=tsclean.sshuser) as c:
            c.get(show["filename"], dest)
        return dest
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def doRadio(show, testing=False):
    """Convert a radio show from the tvheadend server and make an mp3 file from it.

    var testing: the fqfn of a test file - which should be mentioned in the show dict
    if testing is not false the copy will be ignored and the test file used.
    """
    try:
        src = copyRadioFile(show)
        # fn = show["filename"]
        basepath = os.path.splitext(src)[0]
        match = re.search("^[0-9]+/[0-9]+", show["disp_description"])
        titleext = ""
        if match:
            shownumber, totalshows = match[0].split("/")
            titleext = f"_{shownumber}-of-{totalshows}"
        dest = f"{basepath}{titleext}.mp3"
        # basefn = fn.split("/")[-1].split(".")[0]
        # dest = "/".join([os.path.dirname(src), f"{basefn}.mp3"])
        mp3 = makeAudioFile(src, dest)
        if mp3 is None:
            raise Exception(f"failed to create mp3 from {src}")
        os.unlink(src)
        if not testing:
            deleteShow(show)
        audio = EasyID3(mp3)
        audio["genre"] = "Speech"
        audio["title"] = show["disp_title"]
        audio["composer"] = show["disp_description"]
        audio["album"] = show["disp_title"]
        audio["albumartist"] = show["channelname"]
        # match = re.search("^[0-9]+/[0-9]+", show["disp_description"])
        if match:
            audio["tracknumber"], audio["discnumber"] = match[0].split("/")
        audio.save()
        if not testing:
            destdir = f"{os.path.abspath(os.path.expanduser(tsclean.radiooutputdir))}/{show['channelname']}/{show['disp_title']}"
            os.makedirs(destdir, exist_ok=True)
            dest = "/".join([destdir, os.path.basename(mp3)])
            while os.path.exists(dest):
                dest = incrementFileName(dest, addnumber=True)
            os.rename(mp3, dest)
        else:
            dest = mp3
        return dest
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
