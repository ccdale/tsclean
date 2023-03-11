import json
import os
import sys

from tsclean import appname, errorNotify


def getConfig():
    try:
        fn = os.path.abspath(os.path.expanduser(f"~/.config/{appname}.cfg"))
        # print(fn)
        if os.path.exists(fn):
            # print(f"reporting existence of {fn}")
            with open(fn, "r") as ifn:
                cfg = json.load(ifn)
            # print(f"loaded config: {cfg}")
            return cfg
        return {}
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
