import logging

import discord.opus

logger = logging.getLogger(__name__)

def check_and_initialise_opus():
    """Check if Opus is loaded, and initialize it if necessary."""
    if not discord.opus.is_loaded():
        try:
            discord.opus.load_opus('libopus.so.0')  # Works for Linux/Alpine environments
            logger.info("Opus library successfully loaded.")
        except Exception as e:
            logger.error(f"Failed to load Opus library: {e}")
            raise
    else:
        logger.info("Opus library already loaded.")
