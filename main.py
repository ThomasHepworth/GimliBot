import asyncio
import logging
import os

from discord.ext import commands

from src.bot_intents import generate_music_bot_intents
from src.cogs import HelperCommands, MusicCog

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to load bot cogs
async def load_cogs(bot):
    logger.info("Loading cogs...")
    await bot.add_cog(MusicCog(bot))
    logger.info("Cogs loaded successfully.")


# Main bot setup and run logic
async def main():
    logger.info("Initializing bot...")
    bot = commands.Bot(
        command_prefix="!",
        help_command=HelperCommands(),
        intents=generate_music_bot_intents(),
    )

    # Load cogs
    await load_cogs(bot)

    # Retrieve bot token
    token = os.getenv("TOKEN")
    if not token:
        logger.error("No bot token found. Please set the TOKEN environment variable.")
        return

    # Start the bot
    try:
        logger.info("Starting bot...")
        await bot.start(token)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
