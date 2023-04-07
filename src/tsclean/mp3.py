import argparse
import os
import sys

import tsclean
from tsclean import errorExit, errorNotify, errorRaise


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
        parser.add_argument("-t", "--title", help="Title of the track")
        parser.add_argument("-a", "--album", help="album name")
        parser.add_argument("-g", "--genre", help="track genre")
        parser.add_argument("-A", "--artist", help="Artist name")
        parser.add_argument("-n", "--tracknumber", help="tracknumber within the album")
        parser.add_argument(
            "filename", help="path and filename of file to extract audio from."
        )
        args = parser.parse_args()
        # filename = " ".join(args.filename)
        filename = args.filename.strip()
        filename = os.path.abspath(os.path.expanduser(filename))
        if not os.path.exists(filename):
            raise Exception(f"file {filename} does not exist")
        return filename, args
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def ytmp3():
    try:
        filename, args = parseInput()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


if __name__ == "__main__":
    ytmp3()
