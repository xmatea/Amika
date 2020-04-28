import discord
from discord.ext import commands
import datetime

from mongo import db as mongo
from utils.process import readjson
speech = readjson('speech.json')
db = mongo.db

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.hidden = True

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        mongo.insert(guild, mongo.guildModel, db.guilds)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        mongo.remove(guild, db.guilds)

    # in the future, push guild id in array on insert, and check array length to determine removal.
    # only inserting to user db when required...
    @commands.Cog.listener()
    async def on_member_join(self, member):
       pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass        

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(speech.err.noperm.format(error.missing_perms))

        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(speech.err.botnoperm.format(error.missing_perms))
            # if not ctx.channel.permissions_for(ctx.guild.me).send_messages 
        
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            hours = round(seconds // 3600)
            minutes = round((seconds % 3600) // 60)
            seconds = round(seconds % 60)
            return await ctx.send(f"This command is on cooldown, so you'll have to wait a little.... Time remaining: {hours}:{minutes}:{seconds}")
        
        
def setup(bot):
    bot.add_cog(EventHandler(bot))