import discord


def generate_music_bot_intents() -> discord.Intents:
    intents = discord.Intents.default()
    # Allow sending of messages, accessing voice states, and accessing guilds
    intents.messages = True
    intents.guilds = True
    intents.voice_states = True
    return intents
