import argparse
import os
import sys

from tsclean import __version__, errorExit, errorNotify, errorRaise
from tsclean.ffmpeg import tsClean, makeAudioFile
from tsclean.filename import splitFqfn


def parseInput():
    """Parses any command line arguments"""
    try:
        parser = argparse.ArgumentParser(
            description="Clean broadcast transport stream files recorded from Freeview (UK DVB)."
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {__version__}"
        )
        parser.add_argument(
            "-f",
            "--force",
            help="Overwrite input file with output file if sanity tests pass.",
            action="store_true",
        )
        parser.add_argument("filename", help="path and filename of file to clean.")
        args = parser.parse_args()
        # filename = " ".join(args.filename)
        filename = args.filename.strip()
        filename = os.path.abspath(os.path.expanduser(filename))
        if not os.path.exists(filename):
            raise Exception(f"file {filename} does not exist")
        return filename, args.force
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def doClean():
    try:
        filename, force = parseInput()
        ofn = tsClean(filename)
        if os.path.exists(ofn) and force:
            os.rename(ofn, filename)
        sys.exit(0)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def doAudio():
    try:
        filename, force = parseInput()
        fdir, bfn, ext = splitFqfn(filename)
        dest = os.path.join(fdir, f"{bfn}.mp2")
        ndest = makeAudioFile(filename, dest)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def doMp3():
    try:
        filename, force = parseInput()
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
        pass
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
