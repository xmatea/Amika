import discord
from discord.ext import commands
from utils.process import readjson

Config = readjson('config.json')
speech = readjson('speech.json')

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.name = 'Help'

    @commands.command(help=speech.help.help, brief=speech.brief.help)
    async def help(self, ctx, *args):    
        if not args:
            # List all commands in an embed
            embed = discord.Embed(title=":hibiscus: ♡ Help ♡ :hibiscus:",colour=15643828)
            embed.description = f"{speech.helptxt.desc}\n\n".format(ctx.author.name, Config.prefix)

            for c in self.bot.cogs:
                cog = self.bot.get_cog(c)
                if not cog.hidden:
                    text=""
                    for cmd in cog.get_commands():
                        if not cmd.hidden:                       
                            text += f"{Config.prefix}{cmd.name}\n"
                    embed.add_field(name=c, value=text)
            await ctx.send(content="", embed=embed)
        
        elif len(args) > 1:
            await ctx.send("You're making it hard for me... Please specify only one command or category, and I'll help you with that.")
        
        
        elif self.bot.get_cog(args[0].lower().capitalize()):
            cog = self.bot.get_cog(args[0].lower().capitalize())
            if not cog.hidden:
                text=""
                embed = discord.Embed(title=f":hibiscus: ♡ {cog.name} commands ♡ :hibiscus:",colour=15643828)
                for cmd in cog.get_commands():
                    if not cmd.hidden:                       
                        text += f"{cmd.name} - {cmd.brief}\n"
                embed.add_field(name="List of commands", value=text)
                await ctx.send(content="", embed=embed)
                return
        
        elif self.bot.get_command(args[0].lower()):
            cmd = self.bot.get_command(args[0].lower())
            if not cmd.hidden:
                embed = discord.Embed(title=f":hibiscus: ♡ {cmd.name} ♡ :hibiscus:",colour=15643828)               
                text = f"{cmd.help}".format(Config.prefix)
                embed.add_field(name="Help and usage", value=text)
                await ctx.send(content="", embed=embed)
                return

        else:
            await ctx.send("I'm sorry, I can't find that command...")
    
def setup(bot):
    bot.add_cog(Help(bot))