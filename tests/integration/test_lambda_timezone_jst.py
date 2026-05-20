"""Integration test for JST timestamp formatting."""

from datetime import datetime, timezone, timedelta

from src.lambda_function import _get_jst_time_hhmm


def test_get_jst_time_hhmm_matches_utc_plus_9():
    actual = _get_jst_time_hhmm()

    expected = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=9)).strftime(
        "%H:%M"
    )

    assert actual == expected
