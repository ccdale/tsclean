import sys

from tsclean import errorNotify


def reduceTime(unit, secs):
    try:
        rem = 0
        units = 0
        if unit > 0:
            units = int(secs / unit)
            rem = secs % unit
        return units, rem
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def hms(secs):
    try:
        oneday = 86400
        onehour = 3600
        oneminute = 60
        days, rem = reduceTime(oneday, secs)
        hours, rem = reduceTime(onehour, rem)
        minutes, seconds = reduceTime(oneminute, rem)
        return (days, hours, minutes, seconds)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def secondsFromHMS(shms):
    """
    convert "01:02:32.47" to seconds
    """
    try:
        hrs = mins = secs = extra = 0
        xtmp = shms.split(".")
        if int(xtmp[1]) > 50:
            extra = 1
        tmp = xtmp[0].split(":")
        cn = len(tmp)
        if cn == 3:
            hrs = int(tmp[0])
            mins = int(tmp[1])
            secs = int(tmp[2])
        elif cn == 2:
            mins = int(tmp[0])
            secs = int(tmp[1])
        elif cn == 1:
            secs = int(tmp[0])
        return (hrs * 3600) + (mins * 60) + secs + extra
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
