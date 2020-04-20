import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

from mongo import db
import utils.process as process

Config = process.readjson('config.json')
speech = process.readjson('speech.json')
class Moderation(commands.Cog):  
    def __init__(self, bot): 
        self.bot = bot
        self.hidden = False
        self.name = 'Moderation'

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(help=speech.help.clear, brief=speech.brief.clear)
    async def clear(self, ctx, args):
        if not args:
            return await ctx.send("You need to specify a number of messages.")
        try:
            a = int(args)+1
            if a>=1000:
                return await ctx.send("Woah easy, just how many messages do you wanna delete?? Do like 999 or smt, jeez :/")
            d = await ctx.channel.purge(limit=a)
            await ctx.send(f"Deleted {len(d)-1} messages!")
        except ValueError:
            await ctx.send("That's not a number, silly!")
            return
    
    @commands.group(help=speech.help.autodelete,brief=speech.brief.autodelete,hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def autodelete(self, ctx):
        if not ctx.guild.id in Config.ownerguilds:
            return
    
        if ctx.invoked_subcommand is None:
            await ctx.send(speech.help.autodelete)

    @autodelete.command()
    async def start(self, ctx, args):    
        channelobj = ctx.guild.get_channel(int(args))
        if channelobj:
            db.updateGuild(ctx.guild.id, {'$push': {'config.autodelete': channelobj.id}})
            await ctx.send("Started autodeletion in {0}!".format(ctx.guild.get_channel(int(args))))
        else:
            await ctx.send(speech.err.invalidid)
            return
       
    @autodelete.command()
    async def stop(self, ctx, args): 

        channelobj = ctx.guild.get_channel(int(args))
        if channelobj:
            db.updateGuild(ctx.guild.id, {'$pull': {'config.autodelete': channelobj.id}})
            await ctx.send("Stopped autodeletion in {0}!".format(ctx.guild.get_channel(int(args))))
        else:
            await ctx.send(speech.err.invalidid)

    @autodelete.error
    async def autodelete_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(speech.err.noperm.format(ctx.author.name, 'manage_messages'))
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(speech.err.botnoperm, 'manage_messages')

def setup(bot):
    bot.add_cog(Moderation(bot))