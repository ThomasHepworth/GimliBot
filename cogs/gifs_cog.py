import discord
from discord.ext import commands
from cogs.utils.utils import try_delete
import random

gif_roulette = [
    "https://i.gifer.com/embedded/download/upE.gif",
    "https://gfycat.com/softalarmingcaterpillar",
    "https://c.tenor.com/cVVSLto4Jd4AAAAM/tiktok-cat.gif",
    "https://c.tenor.com/YthRIGZYgtwAAAAd/dnd-dungeons-and-dragons.gif",
    "https://c.tenor.com/tenSuG53nc8AAAAS/dance-dungeons-and-dragons.gif",
]

class Gifs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='gif')
    async def _send_d_n_d_gif(self, ctx: commands.Context, *, gif_key = -1):
        """Sends a random dnd gif"""

        # force gif key back to normal if invalid
        if gif_key > len(gif_roulette)-1:
            gif_key=-1
        r = random.randint(0, len(gif_roulette)-1) if gif_key == -1 else gif_key
        gif_out = gif_roulette[r]

        await try_delete(ctx.message)
        await ctx.send(gif_out)

    @commands.command(name='dan_roll')
    async def _send_dan_gif(self, ctx: commands.Context):
        """When Dan rolls..."""
        gif_out = "https://i.gifer.com/1MG0.gif"

        await ctx.send(gif_out)
