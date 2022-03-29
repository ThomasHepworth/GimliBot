import asyncio
import functools
import itertools
import math
import random
from collections import namedtuple
from datetime import datetime, timedelta

import discord
# from async_timeout import timeout
from discord.ext import commands


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='d', aliases = ['d', 'dice', 'r'])
    async def _dice_roll(self, ctx: commands.Context):
        """Rolls a dice"""
#         if message.author.bot:
#             return
#         await ctx.message.add_reaction('🕊️')

# random.randint(1,20)