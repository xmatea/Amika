import discord
from discord.ext import commands
from mongo import db as mongo
import utils.process as process
Config = process.readjson('config.json')
speech = process.readjson('speech.json')
db = mongo.db

class Personal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.name = 'Personal'
                
    @commands.command()
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        user = ctx.author
        mongo.insert(user, mongo.userModel, db.users)

        mongo.update({"_id": user.id}, {'$inc': {"bal": 5}}, db.users)
        embed = discord.Embed(title=":hibiscus: :tooth: Daily teeth :tooth: :hibiscus:", description="Gave {0} **5** teeth! \nCome back in **24** hours for a new claim <3".format(user.name))
        await ctx.send(content="", embed=embed)

    @commands.command(alias="bal")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        user = ctx.author

        mongo.insert(user, mongo.userModel, db.users)
        bal = mongo.find({"_id": user.id}, db.users)['bal']
        
        embed = discord.Embed(title=":hibiscus: {0}'s balance :hibiscus:".format(user.name), description="You can use teeth to buy items or upgrades for me!")
        embed.add_field(name="Teeth", value=f"{bal}:tooth:")
        embed.add_field(name="Want more?", value=f"Get teeth with daily commands, from crates, or by voting for me on top.gg <3 To get a vote link, run {Config.prefix}vote. Remember that you can only vote once per 12 hours...")
        await ctx.send(content="", embed=embed)

def setup(bot):                       
    bot.add_cog(Personal(bot))