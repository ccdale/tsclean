import os

import tsclean
from tsclean.config import getConfig
from tsclean.ffmpeg import fileInfo
from tsclean.radio import copyRadioFile, doRadio
from tsclean.tvh import getRadioRecorded


def test_copyRadioFile():
    show = {
        "filename": "/home/chris/.config/tsradio/testradio.ts",
        "disp_title": "this is a test ts file",
        "disp_description": "2/19 this test file is about 40 seconds of radio",
        "channelname": "testchannel",
    }
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    tsclean.sshuser = cfg.get("sshuser", "")
    tsclean.sshhost = cfg.get("sshhost", "")
    tsclean.radiooutputdir = "/tmp"
    cdest = copyRadioFile(show)
    dest = "/tmp/testradio.ts"
    assert cdest == dest
    assert os.path.exists(dest)


def test_doRadio():
    show = {
        "filename": "/home/chris/.config/tsradio/testradio.ts",
        "disp_title": "this is a test ts file",
        "disp_description": "2/19 this test file is about 40 seconds of radio",
        "channelname": "testchannel",
    }
    cfg = getConfig()
    tsclean.tvhipaddr = cfg.get("tvhipaddr", "")
    tsclean.tvhuser = cfg.get("tvhuser", "")
    tsclean.tvhpass = cfg.get("tvhpass", "")
    tsclean.sshuser = cfg.get("sshuser", "")
    tsclean.sshhost = cfg.get("sshhost", "")
    tsclean.radiooutputdir = "/tmp"
    mp3 = doRadio(show, testing=True)
    assert os.path.exists(mp3)
    finfo = fileInfo(mp3, showtags=True)
    print(finfo)
    assert "format" in finfo
    assert "tags" in finfo["format"]
    assert "track" in finfo["format"]["tags"]
    assert int(finfo["format"]["tags"]["track"]) == 2
    assert int(finfo["format"]["tags"]["disc"]) == 19
    assert finfo["format"]["tags"]["title"] == show["disp_title"]
    assert finfo["format"]["tags"]["composer"] == show["disp_description"]
    assert finfo["format"]["tags"]["album_artist"] == show["channelname"]
