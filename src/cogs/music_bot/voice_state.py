from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING
from asyncio.exceptions import TimeoutError

from async_timeout import timeout
from discord.ext import commands

from src.cogs.music_bot.song_queue import SongQueue

if TYPE_CHECKING:
    from src.cogs.music_bot.parse_youtube_input.extract_from_youtube import YtdlSource

logger = logging.getLogger(__name__)


class VoiceState:
    TIMEOUT = 300  # 5-minute timeout for waiting on the next song

    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current_ytdl_source: YtdlSource = None
        self.voice = None
        self.next_ytdl_source: YtdlSource = asyncio.Event()
        self.songs: SongQueue[YtdlSource] = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = asyncio.create_task(self.audio_player_task())

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        self._volume = value

    @property
    def is_playing(self):
        logger.info(            
            f"Voice: {self.voice}"
            f"Connected: {self.voice.is_connected()}"
            f"Current: {self.current_ytdl_source}"
        )
        return self.voice and self.voice.is_connected() and self.current_ytdl_source

    async def audio_player_task(self):
        while True:
            self.next_ytdl_source.clear()
            try:
                if not self.loop:
                    try:
                        async with timeout(self.TIMEOUT):
                            self.current_ytdl_source = await self.songs.get()
                    except TimeoutError:
                        time_elapsed = self.TIMEOUT / 60
                        logger.info(
                            f"No songs in queue for {time_elapsed} minutes. Disconnecting..."
                        )
                        asyncio.create_task(self.stop())
                        return
                    
                current_song = self.current_ytdl_source
                    
                logger.info(f"Attempting to play to playent: {current_song} of type: {type(current_song)}")
                current_song.source.volume = self._volume
                self.voice.play(self.current_ytdl_source.source, after=self.play_next_song)
                await current_song.channel.send(
                    embed=current_song.video_info.create_song_embed(current_song.requester)
                )

                await self.next_ytdl_source.wait()

            except Exception:
                logger.error("Error in audio_player_task:", exc_info=True)
                await self._ctx.send(f"Failed to play song: {current_song}!")
                break

    def play_next_song(self, error=None):
        logging.info(f"Playing the next song in the queue: {self.songs}")
        if error:
            logger.error(f"Error playing song: {error}")
        self.next_ytdl_source.set()

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing:
            logger.info("Skipping the current song.")
            self.voice.stop()

    async def stop(self):
        try:
            self.songs.clear()
        except AttributeError:
            while not self.songs.empty():
                await self.songs.get_nowait()

        if self.audio_player:
            self.audio_player.cancel()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None
