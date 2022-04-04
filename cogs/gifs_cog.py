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
    "https://i.imgur.com/z8zL8lI.gif",
]

gimli_gifs = [
    "https://media3.giphy.com/media/43g7hyj8d8NEY/200w.gif?cid=82a1493bntlkp3u52fkk8d2bo0p09jf4gffi4xus1q76eip2&rid=200w.gif&ct=g",
    "https://img.wattpad.com/48932c272f5e74f280cc7ac458d14fea043e0540/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f5775317833725f6c6157587731773d3d2d3839373639393734312e313631353338326434313834623431633832363434343938333538392e676966",
    "http://33.media.tumblr.com/05acc7337e02831eb0bbff457bea2839/tumblr_njy7692li51u0ngy8o1_400.gif",
    "https://i.pinimg.com/originals/1c/4a/d1/1c4ad1fe6a23178d511405c5cf0189fe.gif"
]

class Gifs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def send_gifs(self, gifs, gif_key):
        # force gif key back to normal if invalid
        if gif_key > len(gifs)-1:
            gif_key=-1
        r = random.randint(0, len(gifs)-1) if gif_key == -1 else gif_key
        return gifs[r]

    @commands.command(name='gif')
    async def _send_d_n_d_gif(self, gifs, ctx: commands.Context, *, gif_key = -1):
        """Sends a random dnd gif"""

        gif_out = self.send_gifs(gif_roulette, gif_key)

        await try_delete(ctx.message)
        await ctx.send(gif_out)

    @commands.command(name='gimli')
    async def _send_gimli_gifs(self, ctx: commands.Context, *, gif_key = -1):
        """Sends a random gimli gif"""

        gif_out = self.send_gifs(gimli_gifs, gif_key)

        await try_delete(ctx.message)
        await ctx.send(gif_out)

    @commands.command(name='dan_roll')
    async def _send_dan_gif(self, ctx: commands.Context):
        """When Dan rolls..."""
        gif_out = "https://i.gifer.com/1MG0.gif"

        await ctx.send(gif_out)
