from __future__ import annotations

import asyncio
import logging
from asyncio.exceptions import TimeoutError

from async_timeout import timeout
from discord.ext import commands

from src.cogs.music_bot.song_queue import SongQueue

logging.basicConfig(level=logging.INFO)


# TODO(ThomasHepworth): Does this logic work?
class VoiceState:
    TIMEOUT = 300  # 5-minute timeout for waiting on the next song

    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

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
        return self.voice and self.voice.is_connected() and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(self.TIMEOUT):
                        self.current = await self.songs.get()
                except TimeoutError:
                    time_elapsed = self.TIMEOUT / 60
                    logging.info(
                        f"No songs in queue for {time_elapsed} minutes. Disconnecting..."
                    )
                    asyncio.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            logging.error(f"Error playing song: {error}")
        self.next.set()

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing:
            logging.info("Skipping the current song.")
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
