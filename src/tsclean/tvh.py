# import json
import sys

import requests
from requests.auth import HTTPDigestAuth

import tsclean
from tsclean import errorExit, errorNotify, errorRaise


class TVHError(Exception):
    pass


def sendToTVH(route, data=None):
    """
    send a request to tvheadend
    """
    try:
        auth = HTTPDigestAuth(tsclean.tvhuser, tsclean.tvhpass)
        # print(f"{auth}")
        url = f"http://{tsclean.tvhipaddr}/api/{route}"
        # print(f"{url}")
        # return None
        r = requests.post(url, data=data, auth=auth)
        if r.status_code != 200:
            raise TVHError("error from tvh: {}".format(r))
        return r.json()
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def getRadioRecorded():
    try:
        route = "dvr/entry/grid_finished"
        recs = sendToTVH(route)
        # with open("grid_finished.json", "w") as ofn:
        # json.dump(recs, ofn, indent=4)
        radiorecs = []
        for rec in recs["entries"]:
            if rec["channelname"].startswith("BBC Radio"):
                radiorecs.append(rec)
        return radiorecs
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def deleteShow(show):
    try:
        route = "dvr/entry/remove"
        dat = {"uuid": show["uuid"]}
        junk = sendToTVH(route, data=dat)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
