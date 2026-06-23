"""`headroom perf` must not crash on a PERF log value that absorbed trailing
JSON-wrapper punctuation (e.g. a line-final `cache_write=88742"}`)."""

from headroom.perf.analyzer import _to_float, _to_int


def test_to_int_strips_trailing_json_wrapper():
    assert _to_int('88742"}') == 88742  # the crash that motivated this
    assert _to_int("88742") == 88742
    assert _to_int("-12,") == -12


def test_to_int_falls_back_on_garbage():
    assert _to_int("", 0) == 0
    assert _to_int('"}', 7) == 7
    assert _to_int(None, 3) == 3
    assert _to_int(0) == 0


def test_to_float_tolerates_trailing_punctuation():
    assert _to_float('1.5"}') == 1.5
    assert _to_float("2") == 2.0
    assert _to_float("x", 0.0) == 0.0
