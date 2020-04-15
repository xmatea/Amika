import discord
from discord.ext import commands
import db
import utils.process as process

Config = process.readjson('config.json')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.name = 'Admin'

    @commands.command(hidden=True)
    async def db_scan(self, ctx, *args):   
        db.insertMembers(ctx.guild.members)
    
    @commands.command(hidden=True)
    async def test(self, ctx, *args):
        db.removeGuild(ctx.guild)

    @commands.command(hidden=True)
    async def gif(self, ctx, *args):
        if args[0] == 'add':
            if ctx.message.author.id in Config.mods:
                gif = args[2:]
                module = args[1]
                c=0
                for g in gif:
                    if g.startswith("https://") and g.endswith(".gif"):
                        db.insertGif(g, module)
                        c+=1
                    else:
                        await ctx.send(f"'{g}' has a bad format and was not accepted. Syntax: `{Config.prefix}gif add [module] [url]`.\n URLs must start with https:// and end with .gif")
                await ctx.send(f"Added {c} gif(s) to the **{args[1]}** gif pool.")
                
def setup(bot):
    bot.add_cog(Admin(bot))