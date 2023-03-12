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
