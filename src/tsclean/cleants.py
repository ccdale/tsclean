import argparse
import os
import sys

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.config import getConfig
from tsclean.comskip import doComSkip
from tsclean.ffmpeg import tsClean, makeAudioFile
from tsclean.filename import splitFqfn
from tsclean.radio import doRadio
from tsclean.tvh import getRadioRecorded


def parseInput():
    """Parses any command line arguments"""
    try:
        parser = argparse.ArgumentParser(
            description="Clean broadcast transport stream files recorded from Freeview (UK DVB)."
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {tsclean.__version__}",
        )
        parser.add_argument(
            "-f",
            "--force",
            help="Overwrite input file with output file if sanity tests pass.",
            action="store_true",
        )
        parser.add_argument("-c", "--channel", help="channel name", default="NOT SET")
        parser.add_argument("filename", help="path and filename of file to clean.")
        args = parser.parse_args()
        # filename = " ".join(args.filename)
        filename = args.filename.strip()
        filename = os.path.abspath(os.path.expanduser(filename))
        if not os.path.exists(filename):
            raise Exception(f"file {filename} does not exist")
        return filename, args.force, args.channel.strip()
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def doClean():
    try:
        filename, force, channel = parseInput()
        ofn = tsClean(filename)
        if os.path.exists(ofn) and force:
            os.rename(ofn, filename)
        if not channel.startswith("BBC"):
            doComSkip(filename)
        sys.exit(0)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def doAudio():
    try:
        filename, force, channel = parseInput()
        fdir, bfn, ext = splitFqfn(filename)
        dest = os.path.join(fdir, f"{bfn}.mp2")
        ndest = makeAudioFile(filename, dest)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def doMp3():
    try:
        filename, force, channel = parseInput()
        fdir, bfn, ext = splitFqfn(filename)
        dest = os.path.join(fdir, f"{bfn}.mp3")
        ndest = makeAudioFile(filename, dest)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def tsRadio():
    """Function to pull radio programmes from tvheadend.

    Radio programmes that tvheadend has recorded from freeview
    (UK DVB).
    """
    try:
        # print("asking for config")
        cfg = getConfig()
        # print(f"{cfg=}")
        tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
        tsclean.tvhuser = cfg.get("tvhuser", "")
        tsclean.tvhpass = cfg.get("tvhpass", "")
        tsclean.radiooutputdir = cfg.get("radiooutputdir", "~/radio")
        tsclean.sshhost = cfg.get("sshhost", "druidmedia")
        tsclean.sshuser = cfg.get("sshuser", "chris")
        # print("Asking for radio")
        rrecs = getRadioRecorded()
        lcn = len(rrecs)
        # print(f"{lcn=}")
        # print("starting loop")
        for cn, rec in enumerate(rrecs):
            print(f"{cn+1:>2}/{lcn} {rec['disp_title']}")
            mp3 = doRadio(rec, testing=False)
            print(f"{mp3=}")
            # break
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
