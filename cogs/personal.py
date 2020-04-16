import discord
from discord.ext import commands
import db
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
                if not ctx.guild.get_member(targetid):
                    raise ValueError
            except ValueError:
                ctx.send(speech.err.invaliduser)
                return
        else:
            targetid = ctx.message.author.id

        member = ctx.guild.get_member(targetid)
        user = db.findMember({"_id":targetid})
        if not user:
            r = db.insertMembers(member)
            user = db.findMember({"_id": r.inserted_id})

        embed = discord.Embed(title=speech.profile.title.format(member.name), colour=process.colour_convert('#8cce51'))

        try:
            bal = user['bal']
        except ValueError:
            bal = 0

        embed.add_field(name="Balance", value=f"Current balance: {bal} :tooth:")
            
        await ctx.send(content="", embed=embed)
                

def setup(bot):
    bot.add_cog(Personal(bot))