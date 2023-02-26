from tsclean.time import reduceTime, hms, secondsFromHMS


def test_reduceTime_hours_exact():
    unit = 3600
    seconds = 7200
    units, rem = reduceTime(unit, seconds)
    assert units == 2
    assert rem == 0


def test_reduceTime_minsplus():
    unit = 60
    seconds = 71
    units, rem = reduceTime(unit, seconds)
    assert units == 1
    assert rem == 11
