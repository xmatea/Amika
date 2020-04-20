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

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after

            hours, rest = divmod(time, 3600)
            minutes, seconds = divmod(rest, 60)
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)

            timestr = f"{hours}h, {minutes}m and {seconds}s"
            embed = discord.Embed(title=":hibiscus: Daily teeth :hibiscus:", description=f"You can only perform this command once every **24** hours... \nThat's capitalism for you :/\nTime remaining: **{timestr}**")
            await ctx.send(content="",embed=embed)
def setup(bot):
    bot.add_cog(Personal(bot))