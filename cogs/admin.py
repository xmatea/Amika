import discord
from discord.ext import commands

from mongo import db
from utils.process import readjson, colour_convert
from utils.checks import isDev

Config = readjson('config.json')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.name = 'Admin'

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def dbScan(self, ctx, *args):   
        db.insertUsers(ctx.guild.members)
        db.insertGuilds(ctx.guild.members)

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
        db.removeGuild(ctx.guild)

    @commands.command(hidden=True)
    @commands.check(isDev)
    async def gif(self, ctx, *args):
        if args[0] == 'add':
            if ctx.message.author.id in Config.mods:
                gif = args[2:]
                module = args[1]
                ret=""
                c=0
                for g in gif:
                    if g.startswith("https://") and g.endswith(".gif"):
                       r = db.insertGif(g, module)
                       d = db.getGif(r.inserted_id)
                       ret += f"ID: {d['_id']}\tURL:`{d['url']}`\n"
                       c+=1
                    else:
                        await ctx.send(f"'{g}' has a bad format and was not accepted. Syntax: `{Config.prefix}gif add [module] [url]`.\n URLs must start with https:// and end with .gif")

                await ctx.send(f"Added {c} gif(s) to the **{args[1]}** gif pool.\n`{ret}`")
                
def setup(bot):
    bot.add_cog(Admin(bot))