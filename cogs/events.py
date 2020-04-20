import discord
from discord.ext import commands
from mongo import db
from utils.process import readjson
speech = readjson('speech.json')

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.hidden = True

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.insertGuilds(guild)
        db.insertUsers(guild.members)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.removeGuild(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not db.queryUsers({"_id": member.id}):
            return db.insertUser(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if db.queryUsers({"_id": member.id}):
            db.removeUser({"_id": member.id})
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(speech.err.noperm.format(error.missing_perms))

        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(speech.err.botnoperm.format(error.missing_perms))
            # if not ctx.channel.permissions_for(ctx.guild.me).send_messages 
        
        if isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after
            time = round(time, 2)
            if ctx.command.name == 'daily':
                hours, rest = divmod(time, 3600)
                minutes, seconds = divmod(rest, 60)
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)

                timestr = f"{hours}h, {minutes}m and {seconds}s"
                embed = discord.Embed(title=":hibiscus: Daily teeth :hibiscus:", description=f"You can only perform this command once every **24** hours... \nThat's capitalism for you :/\nTime remaining: **{timestr}**")
                return await ctx.send(content="",embed=embed)

            await ctx.send(f"Woah there {ctx.message.author.name}, I put you on cooldown... Time remaining: {error.retry_after}s")

def setup(bot):
    bot.add_cog(EventHandler(bot))