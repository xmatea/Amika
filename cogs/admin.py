import discord
from discord.ext import commands

from mongo import db as mongo
from utils.process import readjson, colour_convert
from utils.checks import isDev

db = mongo.db
Config = readjson('config.json')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.name = 'Admin'

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def dbscan(self, ctx, *args):   
        r = mongo.insert(ctx.guild.members, mongo.userModel, db.users)
        await ctx.send(f"inserted {r} docs")

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def colourconvert(self,ctx,*args):
        await ctx.send(colour_convert(args[0]))

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def clonecoll(self, ctx, *args):
        r = db.clonecoll(args[0])
        await ctx.send(f"Scanned {r} documents and added non duplicates into **{args[0]}**")

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def test(self, ctx, *args):
        mongo.insert(ctx.guild, mongo.guildModel, db.guilds)
        mongo.update({"_id": ctx.guild.id}, {'$set': {"vm_enabled": True} }, db.guilds)

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def gif(self, ctx, *args):
        if args[0] == 'add':
            if ctx.message.author.id in Config.devs:
                gif = args[2:]
                module = args[1]
                lis=[]
                for g in gif:
                    if g.startswith("https://") and g.endswith(".gif"):
                       lis.append([g, module])
                    else:
                        await ctx.send(f"'{g}' has a bad format and was not accepted. Syntax: `{Config.prefix}gif add [module] [url]`.\n URLs must start with https:// and end with .gif")
                r = mongo.gifInsert(lis, mongo.gifModel, db.gifs)
                await ctx.send(f"Added {len(r)} gif(s) to the **{args[1]}** gif pool.\n")
                
def setup(bot):
    bot.add_cog(Admin(bot))