from __future__ import annotations

import logging
from typing import Dict, Optional

import discord
from pydantic import BaseModel, Field, HttpUrl, field_validator

from src.cogs.music_bot.parse_youtube_input.parsers import (
    parse_date,
    parse_duration,
    readable_view_count,
)

logger = logging.getLogger(__name__)


class VideoDownloadInfo(BaseModel):
    filesize: Optional[int]
    format_id: Optional[str]
    quality: Optional[str]

    @classmethod
    def parse_video_download_info(cls, video_info: Dict[str, str]) -> VideoDownloadInfo:
        return cls(
            filesize=video_info.get("filesize"),
            format_id=video_info.get("format_id"),
            quality=video_info.get("quality"),
        )


# TODO(ThomasHepworth): Add some tests for this class.
class VideoInfo(BaseModel):
    title: str
    thumbnail: HttpUrl
    duration: int = Field(..., gt=0, description="Video duration in seconds.")
    webpage_url: HttpUrl
    stream_url: HttpUrl
    view_count: int = Field(..., ge=0, description="Total video view count.")
    upload_date: str
    download_info: Optional[VideoDownloadInfo] = None

    @field_validator("upload_date")
    def validate_upload_date(cls, value):
        if not value.isdigit() or len(value) != 8:
            raise ValueError("Upload date must be in YYYYMMDD format.")
        return value

    @field_validator("duration", mode="after")
    def parse_duration(cls, v):
        return parse_duration(v)

    @field_validator("view_count", mode="after")
    def parse_view_count(cls, v):
        return readable_view_count(v)

    @field_validator("upload_date", mode="after")
    def parse_upload_date(cls, v):
        return parse_date(v)
    
    @field_validator("stream_url", mode="after")
    def change_to_str(cls, value):
        return str(value)

    @classmethod
    def parse_video_information(
        cls, video_info: Dict[str, str], download_info: bool = False
    ) -> VideoInfo:
        """
        Parse the video information from a video metadata dictionary.
        """
        if not video_info:
            raise ValueError("No video information supplied.")

        if video_info.__contains__("entries"):
            video_info = video_info["entries"][0]

        try:
            if download_info:
                video_download_info = VideoDownloadInfo.parse_video_download_info(
                    video_info
                )
            else:
                video_download_info = None

            return cls(
                title=video_info.get("title", "Unknown Title"),
                thumbnail=video_info.get("thumbnail"),
                duration=video_info.get("duration"),
                webpage_url=video_info.get("webpage_url"),
                stream_url=video_info.get("url"),
                view_count=video_info.get("view_count", 0),
                upload_date=video_info.get("upload_date"),
                download_info=video_download_info,
            )
        except Exception as e:
            logging.error(f"Error parsing video information: {e}")
            raise ValueError("Invalid video information format.") from e

    def formatted_log(self) -> str:
        """Return a formatted log string for video information."""
        lines = [
            "Video Information:",
            f"\tTitle: {self.title}",
            f"\tThumbnail: {self.thumbnail}",
            f"\tDuration: {self.duration}",
            f"\tURL: {self.webpage_url}",
            f"\tStream URL: {self.stream_url}",
            f"\tView Count: {self.view_count}",
            f"\tUpload Date: {self.upload_date}",
        ]
        return "\n".join(lines)

    def log_video_information(self):
        """Log the formatted video information."""
        logger.info(self.formatted_log())
        if self.download_info:
            logger.info(self.download_info.formatted_log())

    def create_song_embed(self, requester: discord.Member) -> discord.Embed:
        """
        Create a well-formatted Discord embed for the currently playing song.

        Args:
            video_info (VideoInfo): Parsed video information.
            requester (discord.Member): The Discord member who requested the song.

        Returns:
            discord.Embed: A formatted Discord embed with video information.
        """

        embed = discord.Embed(
            title="🎵  Now Playing  🎵",
            description=f"```yaml\n{self.title}\n```",
            color=discord.Color.blurple(),
        )

        embed.add_field(name="Duration", value=self.duration, inline=True)
        embed.add_field(name="Views", value=self.view_count, inline=True)
        embed.add_field(name="Upload Date", value=self.upload_date, inline=True)
        embed.add_field(name="Requested by", value=requester.mention, inline=True)
        embed.add_field(
            name="Watch URL", value=f"[Click here]({self.webpage_url})", inline=False
        )

        embed.set_thumbnail(url=self.thumbnail)
        embed.set_footer(text="Enjoy your music! 🎧")

        return embed

    def generate_song_queue_embed(self, order: int) -> str:
        """
        Generate a song description for the currently playing song.

        Returns:
            str: A formatted string with song information.
        """
        return (
            f"`{order}.` [**{self.title}**]({self.webpage_url})" f"-- `{self.duration}`"
        )
