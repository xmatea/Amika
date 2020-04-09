import discord
from discord.ext import commands
import utils.database as db

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.name = 'Admin'

def setup(bot):
    bot.add_cog(Admin(bot))