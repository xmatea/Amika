import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

from mongo import db as mongo
from utils.process import readjson, mentionStrip
import re
import random
import mongo.db as db

Config = readjson('config.json')
speech = readjson('speech.json')

class Gifs(commands.Cog):  
    def __init__(self, bot): 
        self.bot = bot
        self.hidden = False
        self.name = 'Gifs'
    
    def gifCaption(self, ctx, target, resp, check):
        if not target:
            return resp.none.format(ctx.message.author.name), True
        try:
            targetid = mentionStrip(target[0])
            target = ctx.guild.get_member(targetid)
            
        except ValueError:
            return resp.err.format(ctx.message.author.name), True

        if target:
            if target.id == ctx.message.author.id:
                return resp.self.format(ctx.message.author.name), True
            if target.id == self.bot.user.id:
                return resp.me.format(ctx.message.author.name), True
            if check:
                if target.id in Config.devs:
                    if not ctx.message.author.id in Config.devs:
                        return speech.isTaken.format(target.name), False

            return resp.user.format(ctx.message.author.name, target.name), True
        return resp.err.format(ctx.message.author.name), True

    @commands.command(hidden=False, help=speech.help.blush, brief=speech.brief.blush)
    async def blush(self, ctx, *args):
        response = self.gifCaption(ctx, target=args, resp=speech.blush, check=True)
        embed = discord.Embed(title=response[0])

        if response[1]:
            gif = mongo.randGif('blush')
            embed.set_image(url=gif)
        
        await ctx.send(content="", embed=embed)

    @commands.command(hidden=False, help=speech.help.cuddle, brief=speech.brief.cuddle)
    async def cuddle(self, ctx, *args): 
        response = self.gifCaption(ctx, target=args, resp=speech.cuddle, check=True)
        embed = discord.Embed(title=response[0])

        if response[1]:
            gif = mongo.randGif('cuddle')
            embed.set_image(url=gif)
        
        await ctx.send(content="", embed=embed)

    @commands.command(hidden=False, help=speech.help.slap, brief=speech.brief.slap)
    async def slap(self, ctx, *args): 
        response = self.gifCaption(ctx, target=args, resp=speech.slap, check=False)
        embed = discord.Embed(title=response[0])

        if response[1]:
            gif = mongo.randGif('slap')
            embed.set_image(url=gif)
        
        await ctx.send(content="", embed=embed)

    @commands.command(hidden=False, help=speech.help.hug, brief=speech.brief.hug)
    async def hug(self, ctx, *args): 
        response = self.gifCaption(ctx, target=args, resp=speech.hug, check=True)
        embed = discord.Embed(title=response[0])

        if response[1]:
            gif = mongo.randGif('hug')
            embed.set_image(url=gif)
        
        await ctx.send(content="", embed=embed)
  
    @commands.command(hidden=False, help=speech.help.kiss, brief=speech.brief.kiss)
    async def kiss(self, ctx, *args): 
        response = self.gifCaption(ctx, target=args, resp=speech.kiss, check=True)
        embed = discord.Embed(title=response[0])

        if response[1]:
            gif = mongo.randGif('kiss')
            embed.set_image(url=gif)
        
        await ctx.send(content="", embed=embed)

def setup(bot):
    bot.add_cog(Gifs(bot))