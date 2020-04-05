import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def scan(self):
        pass

def setup(bot):
    bot.add_cog(Admin(bot))