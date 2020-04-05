import discord
from discord.ext import commands
import utils.database as db

class Moderation(commands.Cog):  
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("hi")

def setup(bot):
    bot.add_cog(Moderation(bot))