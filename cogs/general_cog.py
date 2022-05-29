import discord
from discord.ext import commands
from cogs.utils.utils import try_delete

d_n_d_server = "https://www.owlbear.rodeo/game/XzmZBfoKW"

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='owlbear', aliases = ['rodeo'])
    async def _server_link(self, ctx: commands.Context):
        """Links to the D&D 2d server"""

        def create_embed(ctx):
            embed = (discord.Embed(
                title=f'🎲 Owlbear Rodeo 🎲',
                description="\n\n\n**Get the coffee ready** ☕",
                url=d_n_d_server,
                color=discord.Color.gold())
                .add_field(name='Requested by', value=ctx.author.mention)
                # .set_image(url="https://www.owlbear.rodeo/static/media/Owlington.bb5589cf.png")
                .set_thumbnail(url="https://www.owlbear.rodeo/static/media/Owlington.bb5589cf.png")
                )

            return embed

        # await ctx.send(create_embed, allowed_mentions=discord.AllowedMentions(users=[ctx.author]))
        await try_delete(ctx.message)
        # await ctx.send(create_embed(ctx))
        await ctx.send(embed=create_embed(ctx))
