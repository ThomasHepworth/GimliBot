import pytest
import yt_dlp

from src.cogs.music_bot.parse_youtube_input.extract_from_youtube import (
    VideoInfo,
    extract_video,
    is_valid_youtube_watch_url,
)
from src.parse_json import parse_json


@pytest.fixture
def ytdl_instance():
    ytdl_opts = {**parse_json("config/youtube-dl.json"), **{"quiet": True}}
    return yt_dlp.YoutubeDL(ytdl_opts)


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        # Valid YouTube URLs
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://youtu.be/dQw4w9WgXcQ", True),
        ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", True),
        # Only support watch
        ("https://youtube.com/embed/dQw4w9WgXcQ", False),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", False),
        # Valid, but without a video ID
        ("http://youtu.be", False),
        ("https://youtube.com", False),
        ("https://www.youtube.com/watch?", False),
        # Invalid YouTube URLs
        ("https://example.com/watch?v=dQw4w9WgXcQ", False),
        ("https://www.notyoutube.com/watch?v=dQw4w9WgXcQ", False),
        ("", False),
        ("just some text", False),
        ("https://youtube.com/some/other/path", False),
    ],
)
def test_is_youtube_url(url, expected):
    assert is_valid_youtube_watch_url(url) == expected


@pytest.mark.slow
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "valid_url",
    [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/9bZkp7q19f0",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        "testing",
        "cocomelon",
    ],
)
async def test_extract_video_with_generic_urls(
    ytdl_instance: yt_dlp.YoutubeDL, valid_url: str
):
    """
    Test extract_video to ensure it handles generic valid and
    invalid inputs without error.
    """
    video_info = await extract_video(ytdl_instance, valid_url)
    assert isinstance(
        video_info, VideoInfo
    ), "Returned object should be of type VideoInfo"
    assert video_info.title, "Title should not be empty"


@pytest.mark.slow
@pytest.mark.asyncio
async def test_extract_rickroll(ytdl_instance: yt_dlp.YoutubeDL):
    """
    Test extract_video with the Rickroll URL.
    """
    video_info = await extract_video(
        ytdl_instance, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    assert (
        video_info.title == "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    )
