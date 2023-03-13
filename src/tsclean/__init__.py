import sys

__version__ = "0.5.15"
tvhuser = "unset"
tvhpass = "unset"
tvhipaddr = "druidmedia"
radiooutputdir = "~/radio"
sshhost = "druidmedia"
sshuser = "chris"
appname = "tsclean"


def errorNotify(exci, e, fname=None):
    lineno = exci.tb_lineno
    if fname is None:
        fname = exci.tb_frame.f_code.co_name
    ename = type(e).__name__
    msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
    print(msg)


def errorRaise(exci, e, fname=None):
    errorNotify(exci, e, fname)
    raise


def errorExit(exci, e, fname=None):
    errorNotify(exci, e, fname)
    sys.exit(1)
