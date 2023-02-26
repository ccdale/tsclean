from tsclean.strings import displayValue, displayHMS, displayHMSLong


def test_displayValue_zero():
    assert "" == displayValue(0, "junk")


def test_displayValue_12():
    assert "12 junks" == displayValue(12, "junk")


def test_displayValue_1():
    assert "1 junk" == displayValue(1, "junk")


def test_displayValue_zero_not_zero():
    assert "0 junks" == displayValue(0, "junk", zero=False)


def test_displayHMS():
    assert "1:03:12" == displayHMS(0, 1, 3, 12)


def test_displayHMS_days():
    assert "3:01:31:02" == displayHMS(3, 1, 31, 2)


def test_displayHMSLong():
    assert "1 day 3 hours, 2 minutes and 12 seconds" == displayHMSLong(1, 3, 2, 12)


def test_displayHMSLong_nodays():
    assert "3 hours, 2 minutes and 12 seconds" == displayHMSLong(0, 3, 2, 12)


def test_displayHMSLong_zeros():
    assert "2 days 0 hours, 1 minute and 0 seconds" == displayHMSLong(2, 0, 1, 0)
