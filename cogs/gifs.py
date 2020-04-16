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


class Gifs(commands.Cog):  
    def __init__(self, bot): 
        self.bot = bot
        self.hidden = False
        self.name = 'Gifs'

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


def setup(bot):
    bot.add_cog(Gifs(bot))