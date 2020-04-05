import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("hii")

def setup(bot):
    bot.add_cog(Moderation(bot))