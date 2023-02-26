import os

from tsclean.ffmpeg import (
    extractAudioFromTs,
    fileDuration,
    fileInfo,
    getStreamType,
    hasSubtitles,
    makeAudioFile,
    trackIndexes,
    tsClean,
)
from tsclean.filename import splitFqfn


def test_fileInfo():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    finfo = fileInfo(fqfn)
    assert "streams" in finfo


def test_getSteamType_video():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    finfo = fileInfo(fqfn)
    stream = getStreamType(finfo, stype="video")
    assert "codec_name" in stream
    assert stream["codec_name"] == "mpeg2video"


def test_hasSubtitles():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    finfo = fileInfo(fqfn)
    assert True == hasSubtitles(finfo)


def test_fileDuration():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    finfo = fileInfo(fqfn)
    dur = fileDuration(finfo)
    assert dur > 0
    assert dur == 1810


def test_trackIndexes():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    finfo = fileInfo(fqfn)
    vtrk, atrk, strk = trackIndexes(finfo)
    assert vtrk == 0
    assert atrk == 1
    assert strk == 3


def test_extractAudioFromTs():
    fqfn = os.path.abspath("tests/The-News-Quiz-E08.ts")
    assert True == extractAudioFromTs(fqfn)


def test_makeAudioFile():
    fqfn = os.path.abspath("tests/The-News-Quiz-E08.ts")
    fdir, bfn, ext = splitFqfn(fqfn)
    dest = os.path.join(fdir, f"{bfn}.mp2")
    ndest = makeAudioFile(fqfn, dest)
    assert ndest == dest


def test_tsClean():
    fqfn = os.path.abspath("tests/BBCTVChannel.ts")
    fdir, bfn, ext = splitFqfn(fqfn)
    expecteddest = os.path.join(fdir, f"{bfn}-cleaned{ext}")
    dest = tsClean(fqfn)
    assert dest == expecteddest
