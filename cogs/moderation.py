import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, BotMissingPermissions

from mongo import db as mongo
import utils.process as process
import time

Config = process.readjson('config.json')
speech = process.readjson('speech.json')
db = mongo.db
vcmon_cooldowns = dict()
millis = lambda: int(round(time.time() * 1000))

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

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(administrator=True)
    @commands.group(help=speech.help.vc_monitoring, brief=speech.brief.vc_monitoring, name='vc_monitoring', aliases=['vc_mon'])       
    async def vcmon(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=":hibiscus: Voice chat monitoring :hibiscus:", description=speech.help.vc_monitoring.format(Config.prefix))
            await ctx.send(content="", embed=embed)
           
    @vcmon.command()
    async def set(self, ctx, *args):
        try:
            c,t,d = 0,0,0
            for i in args:
                if i == '-c' or i == '--cooldown':
                    cid = int(args[args.index(i)+1])
                    c = ctx.guild.get_channel(cid)     
                elif i == '-t' or i == '--threshold':
                    t = int(args[args.index(i)+1])
                    if t < 3:
                        await ctx.send("Warning: a threshold of 2 or lower not recommended, and can result in unnecessary pings.")
                elif i == '-d':
                    d = int(args[args.index(i)+1])
                    if d < 10:
                        await ctx.send("Warning: a threshold of less than 10 minutes can cause excessive pings.")
            if not (c and t and d):
                raise IndexError

            r = await ctx.guild.create_role(name='Voice ping')
            mongo.update({"_id": ctx.guild.id}, {'$set': {'vm':{"channel": c.id, "threshold": t, "enabled":True, "role":r.id, 'cooldown':d*60 } } }, db.guilds)         
            await ctx.send(f"Started voice chat monitoring successfully. \nThreshold: `{t}`\nChannel: `{c.name}`\nRole to ping: {r.mention}")
        except (ValueError, IndexError):
            return await ctx.send(speech.err.inputfail.format(Config.prefix, 'vc_monitoring'))

    @vcmon.command()
    async def stop(self, ctx, *args):
        if not mongo.find({"$and":[{"_id": ctx.guild.id}, {"vm.enabled": True}]}, db.guilds):
            return await ctx.send("Voice chat monitoring is not enabled yet in this server.")
        mongo.update({"_id": ctx.guild.id}, {'$set': {'vm.enabled':False } }, db.guilds)
        await ctx.send("Stopped voice chat monitoring in this server.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            d = mongo.find({"$and":[{"_id": member.guild.id}, {"vm.enabled": True}]}, db.guilds)
            if d:
                if not vcmon_cooldowns.get(member.guild.id) or (millis() - vcmon_cooldowns.get(member.guild.id)) > d['vm']['cooldown']:
                    a = len(after.channel.members)
                    print
                    if d['vm']['threshold'] <= a:
                        c = d['vm']['channel']
                        r = d['vm']['role']
                        role = member.guild.get_role(r)
                        if mongo.find({"$and":[{"_id": member.guild.id}, {"language": "no"}]}, db.guilds):
                            await member.guild.get_channel(c).send(f"Hei {role.mention}, ser ut som det skjer noe i voice chats...")
                        else:
                            await member.guild.get_channel(c).send(f"Hey {role.mention}, {a} users are currently in a voice chat")
                        vcmon_cooldowns[member.guild.id] = millis()
def setup(bot):
    bot.add_cog(Moderation(bot))
