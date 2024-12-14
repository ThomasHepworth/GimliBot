# TODO(ThomasHepworth): Add searching functionality.
from __future__ import annotations

import asyncio
import logging
from urllib.parse import parse_qs, urlparse

import discord
import yt_dlp

from src._exceptions import YTDLError
from src.cogs.music_bot.parse_youtube_input.video_info import VideoInfo
from src.parse_json import parse_json

logger = logging.getLogger(__name__)


def is_valid_youtube_watch_url(url: str) -> bool:
    """
    Check if a URL is a valid YouTube video or shorts URL.
    Returns True if valid, False otherwise.
    """
    parsed = urlparse(url)
    valid_domains = {"youtube.com", "youtu.be", "m.youtube.com", "www.youtube.com"}
    # valid_paths = {"/watch", "/embed", "/shorts"}
    valid_paths = {"/watch"}

    if parsed.netloc not in valid_domains:
        return False

    if parsed.netloc == "youtu.be":
        return bool(parsed.path.strip("/"))

    if not any(parsed.path.startswith(path) for path in valid_paths):
        return False

    if parsed.path.startswith("/watch"):
        query_params = parse_qs(parsed.query)
        return "v" in query_params

    return True


async def extract_video(
    ytdl: yt_dlp.YoutubeDL, url: str, download: bool = False
) -> VideoInfo:
    """
    Extract a YouTube video's information using yt_dlp.
    If the URL is not a valid YouTube URL, search for the query instead.
    """
    loop = asyncio.get_running_loop()
    if not is_valid_youtube_watch_url(url):
        url = f"ytsearch:{url}"

    try:
        logger.info(f"Extracting video information for: {url}")
        video_info = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=download)
        )
        if video_info is None:
            raise YTDLError(f"Couldn't find anything that matches: `{url}`")
        logger.info(f"Successfully extracted video information for: {url}")
        logger.debug(f"Video information: {video_info}")
        return VideoInfo.parse_video_information(video_info)
    except Exception as e:
        raise YTDLError(f"Error extracting video information: {str(e)}")


class YtdlSource(discord.PCMVolumeTransformer):
    """
    A class to handle YouTube audio sources.
    """

    YDL_CONFIG = parse_json("config/youtube-dl.json")
    FFMPEG_CONFIG = parse_json("config/ffmpeg.json")
    YTDL = yt_dlp.YoutubeDL(YDL_CONFIG)

    def __init__(
        self,
        source: discord.FFmpegPCMAudio,
        *,
        video_info: VideoInfo,
        volume: float = 0.5,
    ):
        super().__init__(source, volume)
        self.video_info = video_info

    @classmethod
    async def get_from_source(cls, search: str, *, volume: float = 0.5):
        """
        Extract video information and create a Discord-compatible audio source.
        """
        video_info: VideoInfo = await extract_video(cls.YTDL, search)

        # Use the direct streamable URL for FFmpeg
        ffmpeg_options = cls.FFMPEG_CONFIG
        source = discord.FFmpegPCMAudio(video_info.stream_url, **ffmpeg_options)

        return cls(source, video_info=video_info, volume=volume)
