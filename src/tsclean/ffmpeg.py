import json
import os
import subprocess
import sys

from tsclean import errorExit, errorNotify, errorRaise
from tsclean.filename import splitFqfn
from tsclean.shell import listCmd, shellCommand


def fileInfo(fqfn, showtags=False):
    try:
        if os.path.exists(fqfn):
            cmd = [
                "ffprobe",
                "-loglevel",
                "quiet",
                "-of",
                "json",
                "-show_streams",
            ]
            if showtags:
                cmd.append("-show_format")
            cmd.append(fqfn)
            out, err = shellCommand(cmd)
            return json.loads(out)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getStreamType(finfo, stype="video"):
    try:
        if stype == "audio":
            return pickAudio(finfo)
        for stream in finfo["streams"]:
            if "codec_type" in stream and stream["codec_type"] == stype:
                return stream
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def pickAudio(finfo):
    try:
        for stream in finfo["streams"]:
            if "codec_type" in stream and stream["codec_type"] == "audio":
                if (
                    "disposition" in stream
                    and stream["disposition"]["visual_impaired"] == 0
                ):
                    return stream
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def hasSubtitles(finfo):
    try:
        vtrk, atrk, strk = trackIndexes(finfo)
        return False if strk == -1 else True
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def infoDuration(finfo):
    try:
        dur = 0
        stream = getStreamType(finfo, stype="video")
        if stream is not None and "duration" in stream:
            xtmp = stream["duration"].split(".")
            dur = int(xtmp[0])
        return dur
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def trackIndexes(finfo):
    try:
        vtrack = atrack = strack = -1
        for stream in finfo["streams"]:
            if "codec_type" in stream:
                if stream["codec_type"] == "video":
                    vtrack = stream["index"]
                elif stream["codec_type"] == "audio":
                    if (
                        "disposition" in stream
                        and stream["disposition"]["visual_impaired"] == 0
                    ):
                        atrack = stream["index"]
                elif stream["codec_type"] == "subtitle":
                    strack = stream["index"]
        return (vtrack, atrack, strack)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def getTracks(finfo):
    try:
        types = ["video", "audio", "subtitle"]
        trks = {}
        for stream in finfo["streams"]:
            if "codec_type" in stream:
                if stream["codec_type"] in types:
                    if stream["codec_type"] == "audio":
                        if int(stream["channels"]) > 1:
                            trks[stream["codec_type"]] = stream
                    else:
                        trks[stream["codec_type"]] = stream
        return trks
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def extractAudioFromTs(fqfn):
    """Extracts the audio without conversion from a freeview ts file."""
    try:
        if os.path.exists(fqfn):
            fdir, bfn, ext = splitFqfn(fqfn)
            dest = os.path.join(fdir, f"{bfn}.mp2")
            if os.path.exists(dest):
                os.unlink(dest)
            finfo = fileInfo(fqfn)
            trks = trackIndexes(finfo)
            cmd = f"ffmpeg -i {fqfn} -map 0:{trks[1]} -acodec copy {dest}"
            sout, serr = shellCommand(cmd)
            if os.path.exists(dest):
                print("output seems to exist")
                dfinfo = fileInfo(dest)
                print(f"{dfinfo=}")
                vtrk, atrk, strk = trackIndexes(finfo)
                print(f"{vtrk=}, {atrk=}, {strk=}")
                if vtrk == -1 and strk == -1 and atrk >= 0:
                    return True
        return False
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def makeAudioFile(src, dest):
    """Extracts the audio from the media file into the output file.

    will convert the audio depending on the extension of the output file
    """
    try:
        if os.path.exists(src):
            if os.path.exists(dest):
                os.unlink(dest)
            cmd = ["ffmpeg", "-i", src, "-q:a", "4", "-map", "a", dest]
            _, _ = shellCommand(cmd, canfail=True)
            # proc = subprocess.run(cmd)
            # if proc.returncode == 0:
            if os.path.exists(dest):
                return dest
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def buildMappingCommand(tracks):
    try:
        mapping = ""
        types = {"video": "-vcodec", "audio": "-acodec", "subtitle": "-scodec"}
        for xtype in types:
            if xtype in tracks:
                if "index" in tracks[xtype]:
                    mapping += f" -map 0:{tracks[xtype]['index']} {types[xtype]} copy"
        return mapping
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def tsClean(fqfn):
    try:
        fdir, bfn, ext = splitFqfn(fqfn)
        ofn = os.path.join(fdir, f"{bfn}-cleaned{ext}")
        if os.path.exists(ofn):
            os.unlink(ofn)
        finfo = fileInfo(fqfn)
        tracks = getTracks(finfo)
        mapping = buildMappingCommand(tracks)
        cmd = ["ffmpeg", "-i", fqfn]
        cmd.extend(listCmd(mapping))
        cmd.append(ofn)
        sout, serr = shellCommand(cmd)
        print(f"{' '.join(cmd)}\n\nstdout:\n{sout}\n\nstderr:\n{serr}")
        if os.path.exists(ofn):
            dfinfo = fileInfo(ofn)
            compareInfo(finfo, dfinfo)
            return ofn
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def compareInfo(finfo, dfinfo):
    try:
        fdur = infoDuration(finfo)
        dfdur = infoDuration(dfinfo)
        dpc = int((dfdur / fdur) * 100)
        if dpc < 90:
            raise Exception(
                f"cleaned file is too short ({dfdur}s) {dpc}% of original length ({fdur}s)."
            )
        ftracks = getTracks(finfo)
        dftracks = getTracks(dfinfo)
        for xtype in ftracks:
            if xtype not in dftracks:
                raise Exception(f"missing {xtype} track in output file")
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)
