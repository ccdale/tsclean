import json
import os
import subprocess
import sys

from tsclean import errorExit, errorNotify, errorRaise
from tsclean.shell import shellCommand


def fileInfo(fqfn):
    try:
        if os.path.exists(fqfn):
            cmd = [
                "ffprobe",
                "-loglevel",
                "quiet",
                "-of",
                "json",
                "-show_streams",
                fqfn,
            ]
            out, err = shellCommand(cmd)
            return json.loads(out)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getStreamType(finfo, stype="video"):
    try:
        for stream in finfo["streams"]:
            if "codec_type" in stream and stream["codec_type"] == stype:
                return stream
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def hasSubtitles(finfo):
    try:
        return True if getStreamType(finfo, stype="subtitle") else False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def fileDuration(finfo):
    try:
        dur = 0
        stream = getStreamType(finfo, stype="video")
        if stream is not None and "duration" in stream:
            xtmp = stream["duration"].split(".")
            dur = int(xtmp[0])
        return dur
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
