import argparse
import os
import sys

from mutagen.easyid3 import EasyID3

import tsclean
from tsclean import errorExit, errorNotify, errorRaise
from tsclean.ffmpeg import makeAudioFile


def parseInput():
    """Parses any command line arguments"""
    try:
        parser = argparse.ArgumentParser(
            description="Extract the audio from a youtube video, convert it to mp3, tag the mp3."
        )
        parser.add_argument("-A", "--artist", help="Artist name")
        parser.add_argument("-a", "--album", help="album name")
        parser.add_argument("-g", "--genre", help="track genre")
        parser.add_argument("-i", "--input", help="the input path and filename")
        parser.add_argument("-n", "--tracknumber", help="tracknumber within the album")
        parser.add_argument("-t", "--title", help="Title of the track")
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {tsclean.__version__}",
        )
        parser.add_argument("outputfilename", help="the output path and filename")
        args = parser.parse_args()
        # argparser expandsuser and returns an absolute filename for file objects
        if args.input is None:
            raise Exception("Input (-i) file missing, use --help for help.")
        if not os.path.exists(args.input):
            raise Exception(f"input file {args.input} does not exist")
        return args
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


def ytmp3():
    """Extracts the audio from a youtube video, converts it to mp3, tags the mp3."""
    try:
        # argparse (above) returns the following structure (which isn't iterable):
        # args=Namespace(force=False, title=None, album=None,
        #    genre=None, artist=None, tracknumber=None,
        #    filename='/home/chris/somefilename')
        # the members can be accessed by `args.title` etc
        args = parseInput()
        print(f"{args=}")
        mp3 = makeAudioFile(args.input, args.outputfilename)
        if mp3 is None:
            raise Exception(f"failed to create mp3 from {src}")
        audio = EasyID3(mp3)
        if args.title is None:
            audio["title"] = args.title
        if args.album is not None:
            audio["album"] = args.album
        if args.artist is not None:
            audio["artist"] = args.artist
        if args.genre is not None:
            audio["genre"] = args.genre
        if args.tracknumber is not None:
            audio["tracknumber"] = args.tracknumber
        audio.save()
        print(f"created {mp3} from {args.input}")
    except Exception as e:
        errorExit(sys.exc_info()[2], e)
