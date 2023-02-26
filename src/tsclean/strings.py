import sys

from tsclean import errorNotify


def displayValue(val, label, zero=True):
    try:
        if zero and val == 0:
            return ""
        dlabel = label if val == 1 else f"{label}s"
        return f"{val} {dlabel}"
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def displayHMS(days, hours, minutes, seconds):
    try:
        xstr = ""
        if days > 0:
            xstr = f"{days}:{hours:02}"
        else:
            xstr = str(hours)
        return f"{xstr}:{minutes:02}:{seconds:02}"
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def displayHMSLong(days, hours, minutes, seconds):
    try:
        dstr = displayValue(days, "day", zero=True)
        hstr = displayValue(hours, "hour", zero=False)
        mstr = displayValue(minutes, "minute", zero=False)
        sstr = displayValue(seconds, "second", zero=False)
        return f"{dstr} {hstr}, {mstr} and {sstr}".strip()
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
