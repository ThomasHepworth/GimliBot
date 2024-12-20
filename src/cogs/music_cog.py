from __future__ import annotations

import logging
import math

import discord
from discord.ext import commands

from src._exceptions import VoiceError, YTDLError
from src.cogs.music_bot.parse_youtube_input.extract_from_youtube import YtdlSource
from src.cogs.music_bot.parse_youtube_input.parsers import parse_duration
from src.cogs.music_bot.voice_state import VoiceState

logger = logging.getLogger(__name__)


class MusicCog(commands.Cog):
    ITEMS_PER_PAGE = 10

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                "This command can't be used in DM channels."
            )

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name="join", invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="summon")
    @commands.has_permissions(manage_guild=True)
    async def _summon(
        self, ctx: commands.Context, *, channel: discord.VoiceChannel = None
    ):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                "You are neither connected to a voice "
                "channel nor specified a channel to join."
            )

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="leave", aliases=["disconnect", "quit"])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send("Not connected to any voice channel.")

        await ctx.voice_state.stop()
        await ctx.message.add_reaction("🕊️")
        del self.voice_states[ctx.guild.id]

    @commands.command(name="volume")
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        if 0 > volume > 100:
            return await ctx.send("Volume must be between 0 and 100")

        ctx.voice_state.volume = volume / 100
        await ctx.send(f"Volume of the player set to {volume}%")

    @commands.command(name="now", aliases=["current", "playing"])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current_ytdl_source.create_embed())

    @commands.command(name="pause")
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏯")

    @commands.command(name="resume")
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction("⏯")

    @commands.command(name="stop")
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction("⏹")

    @commands.command(name="clear")
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Clears the current queue."""

        ctx.voice_state.songs.clear()
        await ctx.send("Song queue cleared ☕")

    @commands.command(name="skip")  # not currently working
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")

        voter = ctx.message.author
        if voter == ctx.voice_state.current_ytdl_source.requester:
            await ctx.message.add_reaction("⏭")
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction("⏭")
                ctx.voice_state.skip()
            else:
                await ctx.send(f"Skip vote added, currently at **{total_votes}/3**")

        else:
            await ctx.send("You have already voted to skip this song.")

    @commands.command(aliases=["queue", "q"], help="Shows info on the current queue.")
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """
        songs = ctx.voice_state.songs  # Access the song queue
        total_songs = len(songs)

        # Handle empty queue
        if total_songs == 0:
            return await ctx.send("The queue is currently empty.")

        # Pagination setup
        total_pages = math.ceil(total_songs / self.ITEMS_PER_PAGE)
        if page < 1 or page > total_pages:
            return await ctx.send(
                f"Invalid page number. Please choose between 1 and {total_pages}."
            )

        start_index = (page - 1) * self.ITEMS_PER_PAGE
        end_index = start_index + self.ITEMS_PER_PAGE

        # Build the queue display and calculate total duration
        queue_description = []
        total_duration = 0

        for n, song in enumerate(songs[start_index:end_index], start=start_index):
            queue_description.append(song.video_info.generate_song_queue_embed(n + 1))
            total_duration += song.video_info.duration

        logger.info("Queue successfully constructed.")
        # Prepare embed message
        total_duration = parse_duration(total_duration)
        logger.info(f"Total duration of all items in queue: {total_duration}")
        embed = discord.Embed(
            title=f"🎶 Current Queue: {total_duration} remaining 🎶",
            description="\n".join(queue_description),
            color=discord.Color.blurple(),
        )
        embed.set_footer(text=f"Page {page}/{total_pages} | Total duration:")

        await ctx.send(embed=embed)

    @commands.command(name="shuffle")
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction("✅")

    @commands.command(name="remove")
    async def _remove(self, ctx: commands.Context, index: int = 1):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction("✅")

    @commands.command(name="loop")
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction("✅")

    @commands.command(aliases=["play", "p"])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        already_playing = ctx.voice_state.is_playing

        async with ctx.typing():
            try:
                ytdl_source = await YtdlSource.get_from_source(ctx, search)
            except YTDLError as e:
                await ctx.send(
                    f"An error occurred while processing this request: {str(e)}"
                )

            await ctx.voice_state.songs.put(ytdl_source)
            logger.info(f"Current queue: {ctx.voice_state.songs.as_list()}")
            await ctx.message.add_reaction("🎵")
            if already_playing:
                await ctx.send(f"🔊 Queued: {ytdl_source.video_info.title}")

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("You are not connected to any voice channel.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Bot is already in a voice channel.")
