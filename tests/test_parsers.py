import pytest

from src.cogs.music_bot.parse_youtube_input.parsers import (
    parse_date,
    parse_duration,
    readable_view_count,
)


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        (100, "1 minute, 40 seconds"),
        (200, "3 minutes, 20 seconds"),
        (300, "5 minutes, 0 seconds"),
        (2_052_000, "570 hours, 0 minutes, 0 seconds"),
        (2_052_062, "570 hours, 1 minute, 2 seconds"),
    ],
)
def test_parse_duration(duration: int, expected: str):
    assert parse_duration(duration) == expected


@pytest.mark.parametrize(
    ("date_str", "expected"),
    [
        ("20210101", "January 01, 2021"),
        ("20211231", "December 31, 2021"),
        ("20210615", "June 15, 2021"),
        ("20210228", "February 28, 2021"),
    ],
)
def test_parse_date(date_str: str, expected: str):
    assert parse_date(date_str) == expected


@pytest.mark.parametrize(
    ("view_count", "expected"),
    [
        (0, "0 views"),
        (1, "1 view"),
        (23, "23 views"),
        (2_300, "2.3k views"),
        (23_000, "23k views"),
        (23_000_000, "23M views"),
    ],
)
def test_readable_view_count(view_count: int, expected: str):
    assert readable_view_count(view_count) == expected
