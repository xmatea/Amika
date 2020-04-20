import discord
from discord.ext import commands
from mongo import db
import utils.process as process
Config = process.readjson('config.json')
speech = process.readjson('speech.json')

class Personal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.name = 'Personal'

    @commands.command(hidden=False)
    async def profile(self, ctx, *args):
        if args:
            try:
                targetid = process.mentionStrip(args[0])
                member = ctx.guild.get_member(targetid)
                if not member:
                    ctx.send(speech.err.invaliduser)
            except ValueError:
                ctx.send(speech.err.invaliduser)
                return
        else:
            member = ctx.message.author

        user = db.queryUsers({"_id":member.id})
        if not user:
            r = db.insertUser(member)
            user = db.queryUsers({"_id": r.inserted_id})

        embed = discord.Embed(title=speech.profile.title.format(member.name), colour=process.colour_convert('#8cce51'))

        bal = user['bal']
        embed.add_field(name="Balance", value=f"Current balance: {bal} :tooth:")
       
            
        await ctx.send(content="", embed=embed)
                
    @commands.command()
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        member = ctx.message.author.id
        db.updateUser({"_id": member}, {'$inc': {"bal": 5}}, upsert=True)
        embed = discord.Embed(title=":hibiscus: :tooth: Daily teeth :tooth: :hibiscus:", description="Gave {0} **5** teeth! \nCome back in **24** hours for a new claim <3".format(ctx.author.name))
        await ctx.send(content="", embed=embed)

    @commands.command(alias="bal")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        member = ctx.message.author.id
        bal = db.queryUsers({"_id": member})['bal']
        embed = discord.Embed(title=":hibiscus: {0}'s balance :hibiscus:".format(ctx.author.name), description="You can use teeth to buy items or upgrades for me! Get teeth with daily commands, from crates, or by voting for me on {0} using {1}vote".format("link", Config.prefix))
        embed.add_field(name="Teeth", value=f"{bal}:tooth:")
        await ctx.send(content="", embed=embed)

def setup(bot):
    bot.add_cog(Personal(bot))