import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

import utils.database as db
from tinydb import Query
import utils.process as process
import re

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
        clr=15643828
        title = ""
        desc = ""

        if not args:
            await ctx.send(f"Well? What do you want me to embed? See {Config.prefix}help embed if you're unsure.")
            return 

        if args[0] == '-c':
            if len(args[1]) == 7 and args[1].startswith('#'):
                hex = args[1]
                clr = colour_convert(hex)-1
                args = args[2:]
            else:
                await ctx.send(f"Please specify a valid hex colour... See {Config.prefix}help embed if you're unsure.`")
                return

        elif args[0] == '-t':
            rawtxt = " ".join(args[1:])
            try:
                title = re.search('\[(.+?)\]', rawtxt).group(1)
                desc = re.search('\](.*)', rawtxt).group(1)
                args=desc.split(" ")
                
            except AttributeError:
                await ctx.send(f"Titles need to be specified in brackets. See {Config.prefix}help embed if you're unsure.")

            if len(title) >= 60:
                await ctx.send("Titles should not exceed 60 characters.")
                return

        await ctx.send(content="", embed=discord.Embed(title=title, description=" ".join(args), colour=clr))
        if ctx.channel.bot_has_permissions('manage_messages'):
            await ctx.message.delete()

def colour_convert(hex):
            hex = hex.lstrip('#')
            hlen = len(hex)
            rgb = tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
            print(rgb)
            print((rgb[0]<<16) + (rgb[1]<<8) + rgb[2])
            return (rgb[0]<<16) + (rgb[1]<<8) + rgb[2]

def setup(bot):
    bot.add_cog(Fun(bot))