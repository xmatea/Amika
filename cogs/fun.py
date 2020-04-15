import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

import db
from tinydb import Query
import utils.process as process
import re
import random

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
                    clr = colour_convert(args[i+1])
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

        #####################################
        ### GIF COMMANDS BELOW ##############
        #####################################

    @commands.command(hidden=False, help=speech.help.blush, brief=speech.brief.blush)
    async def blush(self, ctx, *args): 
        ok = True
        if not args:
            response = speech.blush.none.format(ctx.message.author.name)
        else:
            try:
                targetid = int(args[0].strip("<@!&>"))
                target = ctx.guild.get_member(targetid)
        
                if target:
                    if target == ctx.message.author:
                        response = speech.blush.self.format(ctx.message.author.name)
                    elif target.id == Config.mods.ryan and ctx.message.author.id != Config.mods.tea:
                        response = speech.hasbf
                        ok = False
                    elif target.id == Config.mods.tea and ctx.message.author.id != Config.mods.ryan:
                        response = speech.hasgf
                        ok = False
                    elif target == self.bot.user:
                        response = speech.blush.me.format(ctx.message.author.name)
                    else:
                        response = speech.blush.user.format(ctx.message.author.name, target.name)
                else:
                    response = speech.blush.err.format(ctx.message.author.name)
            except ValueError:
                response = speech.blush.err.format(ctx.message.author.name)

        if ok:
            gif = db.randGif('blush')
            embed = discord.Embed(title=response).set_image(url=gif)
            await ctx.send(content="", embed=embed)
        else:
            await ctx.send(response)

    @commands.command(hidden=False, help=speech.help.cuddle, brief=speech.brief.cuddle)
    async def cuddle(self, ctx, *args): 
        ok = True
        if not args:
            response = speech.cuddle.none.format(ctx.message.author.name)
        else:
            try:
                targetid = int(args[0].strip("<@!&>"))
                target = ctx.guild.get_member(targetid)
        
                if target:
                    if target == ctx.message.author:
                        response = speech.cuddle.self.format(ctx.message.author.name)
                    elif target.id == Config.mods.ryan and ctx.message.author.id != Config.mods.tea:
                        response = speech.hasbf
                        ok = False
                    elif target.id == Config.mods.tea and ctx.message.author.id != Config.mods.ryan:
                        response = speech.hasgf
                        ok = False
                    elif target == self.bot.user:
                        response = speech.cuddle.me.format(ctx.message.author.name)
                    else:
                        response = speech.cuddle.user.format(ctx.message.author.name, target.name)
                else:
                    response = speech.cuddle.err.format(ctx.message.author.name)
            except ValueError:
                response = speech.cuddle.err.format(ctx.message.author.name)

        if ok:
            gif = db.randGif('cuddle')
            embed = discord.Embed(title=response).set_image(url=gif)
            await ctx.send(content="", embed=embed)
        else:
            await ctx.send(response)
    
    @commands.command(hidden=False, help=speech.help.slap, brief=speech.brief.slap)
    async def slap(self, ctx, *args): 
        if not args:
            response = speech.slap.none.format(ctx.message.author.name)
        else:
            try:
                targetid = int(args[0].strip("<@!&>"))
                target = ctx.guild.get_member(targetid)
        
                if target:
                    if target == ctx.message.author:
                        response = speech.slap.self.format(ctx.message.author.name)
                    elif target == self.bot.user:
                        response = speech.slap.me.format(ctx.message.author.name)
                    else:
                        response = speech.slap.user.format(ctx.message.author.name, target.name)
                else:
                    response = speech.slap.err.format(ctx.message.author.name)
            except ValueError:
                response = speech.slap.err.format(ctx.message.author.name)

        gif = db.randGif('slap')
        await ctx.send(content="", embed=discord.Embed(title=response).set_image(url=gif))

    @commands.command(hidden=False, help=speech.help.hug, brief=speech.brief.hug)
    async def hug(self, ctx, *args): 
        ok = True
        if not args:
            response = speech.hug.none.format(ctx.message.author.name)
        else:
            try:
                targetid = int(args[0].strip("<@!&>"))
                target = ctx.guild.get_member(targetid)
        
                if target:
                    if target == ctx.message.author:
                        response = speech.hug.self.format(ctx.message.author.name)
                    elif target.id == Config.mods.ryan and ctx.message.author.id != Config.mods.tea:
                        response = speech.hasbf
                        ok = False
                    elif target.id == Config.mods.tea and ctx.message.author.id != Config.mods.ryan:
                        response = speech.hasgf
                        ok = False
                    elif target == self.bot.user:
                        response = speech.hug.me.format(ctx.message.author.name)
                    else:
                        response = speech.hug.user.format(ctx.message.author.name, target.name)
                else:
                    response = speech.hug.err.format(ctx.message.author.name)
            except ValueError:
                response = speech.hug.err.format(ctx.message.author.name)

        if ok:
            gif = db.randGif('hug')
            embed = discord.Embed(title=response).set_image(url=gif)
            await ctx.send(content="", embed=embed)
        else:
            await ctx.send(response)
    
    @commands.command(hidden=False, help=speech.help.kiss, brief=speech.brief.kiss)
    async def kiss(self, ctx, *args): 
        ok = True
        if not args:
            response = speech.kiss.none.format(ctx.message.author.name)
        else:
            try:
                targetid = int(args[0].strip("<@!&>"))
                target = ctx.guild.get_member(targetid)
                if target:
                    if target == ctx.message.author:
                        response = speech.kiss.self.format(ctx.message.author.name)
                    elif target.id == Config.mods.ryan and ctx.message.author.id != Config.mods.tea:
                        response = speech.hasbf
                        ok = False
                    elif target.id == Config.mods.tea and ctx.message.author.id != Config.mods.ryan:
                        response = speech.hasgf
                        ok = False
                    elif target == self.bot.user:
                        response = speech.kiss.me.format(ctx.message.author.name)
                    else:
                        response = speech.kiss.user.format(ctx.message.author.name, target.name)
                else:
                    response = speech.kiss.err.format(ctx.message.author.name)
            except ValueError:
                response = speech.kiss.err.format(ctx.message.author.name)

        if ok:
            gif = db.randGif('kiss')
            embed = discord.Embed(title=response).set_image(url=gif)
            await ctx.send(content="", embed=embed)
        else:
            await ctx.send(response)

def colour_convert(hex):
            hex = hex.lstrip('#')
            hlen = len(hex)     
            rgb = tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
            ival = (rgb[0]<<16) + (rgb[1]<<8) + rgb[2]
            if ival == 16777215:
                ival -= 1
            return ival

def setup(bot):
    bot.add_cog(Fun(bot))