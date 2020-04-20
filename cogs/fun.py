import discord
import re
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

from mongo import db
import utils.process as process

Config = process.readjson('config.json')
speech = process.readjson('speech.json')

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.name = 'Fun'

    @commands.command(hidden=False, help=speech.help.say, brief=speech.brief.say)
    async def say(self, ctx, *args):
        if not args:
            await ctx.send("Well? What do you want me to say?")
            return
        await ctx.send(" ".join(args))
        await ctx.message.delete()

    @commands.command(hidden=False, help=speech.help.embed, brief=speech.brief.embed)
    async def embed(self, ctx, *args):
        if not args:
            await ctx.send(f"Well? What do you want me to embed? See {Config.prefix}help embed if you're unsure.")
            return

        clr=15643828
        title = ""
        desc = args

        i = 0
        while i < len(args):
            if args[i] == '-c':
                if len(args[i+1]) == 7 and args[i+1].startswith('#'):
                    clr = process.colour_convert(args[i+1])
                    desc = desc[2:]
                    print(desc)
                else:
                    await ctx.send(f"Please specify a valid hex colour... See {Config.prefix}help embed if you're unsure.")
                    return

            elif args[i] == '-t':
                try:
                    title = re.search('\[(.+?)\]', " ".join(args[i+1:])).group(1).split(" ")
                    desc = desc[len(title)+1:]
                except AttributeError:
                    await ctx.send(f"Titles need to be specified in brackets. See {Config.prefix}help embed if you're unsure.")
                    return
                
                if len(title) >= 60:
                    await ctx.send("Titles should not exceed 60 characters.")
                    return
            i-=-1

        desc = " ".join(desc)
        title = " ".join(title)
        await ctx.send(content="", embed=discord.Embed(title=title, description=desc, colour=clr))
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Fun(bot))