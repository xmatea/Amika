import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

import utils.database as db
from tinydb import Query
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
            await ctx.send("You need to specify a number of messages.")
            return

        try:
            a = int(args)+1
            if a>=1000:
                await ctx.send("Woah easy, just how many messages do you wanna delete?? Do like 999 or smt, jeez :/")
                return
            d = await ctx.channel.purge(limit=a)
            await ctx.send(f"Deleted {len(d)-1} messages!")
        except ValueError:
            await ctx.send("That's not a number, silly!")
            return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(speech.err.noperm.format(ctx.author.name, 'administrator'))
            if not self.bot.bot_has_permissions(manage_messages=True):
                await ctx.send(speech.err.botnoperm.format('manage_messages'))


    # [NICHE FEATURE] auto deletion of text in whitelisted channels - will scale horribly
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == Config.ownerguild:
            if not message.author == self.bot.user:
                if (db.queryGuild(Query().config.autodelete, message.channel.id)):
                    if message.content :
                        await message.delete()

    @commands.group(help=speech.help.autodelete,brief=speech.brief.autodelete,hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def autodelete(self, ctx):
        if not ctx.message.guild.id == Config.ownerguild:
            return
    
        if ctx.invoked_subcommand is None:
            await ctx.send("usage ...")

    @autodelete.command()
    async def start(self, ctx, args):    

        guildobj = ctx.guild.get_channel(int(args))
        if not guildobj:
            await ctx.send(speech.err.invalidid)
            return

        doc = db.getGuild(ctx.guild)
        if not doc: 
            db.insertGuild(ctx.guild)
        else:
            db.upsertGuild({'config':{'autodelete': guildobj.id}}, Query().id, ctx.guild.id)
            await ctx.send("Started autodeletion in {0}!".format(ctx.guild.get_channel(int(args))))
       
    @autodelete.command()
    async def stop(self, ctx, args): 

        guildobj = ctx.guild.get_channel(int(args))
        if not guildobj:
            await ctx.send(speech.err.invalidid)
            return

        doc = db.getGuild(ctx.guild)
        if not doc: 
            db.insertGuild(ctx.guild)
        else:
            db.upsertGuild({'config':{'autodelete': guildobj.id}}, Query().id, ctx.guild.id)
            await ctx.send("Stopped autodeletion in {0}!".format(ctx.guild.get_channel(int(args))))

    @autodelete.error
    async def autodelete_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(speech.err.noperm.format(ctx.author.name, 'manage_messages'))
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(speech.err.botnoperm, 'manage_messages')

def setup(bot):
    bot.add_cog(Moderation(bot))