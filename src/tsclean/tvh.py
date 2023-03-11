import sys

import requests

from tsclean import errorExit, errorNotify, errorRaise, tvhipaddr, tvhpass, tvhuser


class TVHError(Exception):
    pass


def sendToTVH(route, data=None):
    """
    send a request to tvheadend
    """
    try:
        auth = (tvheadend.user, tvheadend.passw)
        url = f"http://{tvheadend.ipaddr}/api/{route}"
        r = requests.post(url, data=data, auth=auth)
        if r.status_code != 200:
            raise TVHError("error from tvh: {}".format(r))
        return r.json()
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)
