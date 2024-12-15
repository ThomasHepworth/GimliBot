import os
import logging
from typing import List

import discord
from discord.ext import commands

from src.cogs.music_cog import MusicCog
from src.cogs.test_cog import GifCog
from src.initialisation import check_and_initialise_opus

logger = logging.getLogger(__name__)

async def load_cogs(bot, cogs: List[commands.Cog]):
    for cog in cogs:
        await bot.add_cog(cog(bot))
        logger.info(f"{cog.__name__} loaded successfully.")

async def main():
    check_and_initialise_opus()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Bot is online! Logged in as {bot.user.name}")

    @bot.event
    async def on_command_error(ctx, error):
        """Logs command errors with full traceback."""
        if isinstance(error, commands.CommandNotFound):
            logger.warning(f"Command not found: {ctx.message.content}")
        else:
            logger.error("An error occurred during command execution:", exc_info=error)
            await ctx.send("An unexpected error occurred. Check the logs for details.")

    token = os.getenv("TOKEN")
    if not token:
        logger.error("No bot token found. Set the TOKEN environment variable.")
        return

    await load_cogs(bot, [GifCog, MusicCog])
    await bot.start(token)

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shut down gracefully.")
