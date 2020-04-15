import discord
import flask
from discord.ext import commands
from datetime import date, datetime
from dotenv import load_dotenv
import os
import logging
import utils.process as process
import db


logging.basicConfig(level=logging.INFO)
Config = process.readjson('config.json')

load_dotenv()
TOKEN = os.getenv("TOKEN")

class Amika(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None)
        self.command_prefix = Config.prefix

bot = Amika()

# read and loag cogs
bot.remove_command('help')
bot.remove_cog('general')
for file in os.listdir("cogs"):
    if file.endswith('.py'):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        

@bot.event
async def on_ready():
    print("Amika started at {0}, loaded {1} cog(s)".format(datetime.now().strftime("%H:%M:%S"), len(bot.cogs)))

### event handling ####
@bot.event
async def on_guild_join(guild):
    db.insertGuilds(guild)
    db.insertMembers(guild.members)

@bot.event
async def on_guild_remove(guild):
    db.removeGuild(guild)

@bot.event
async def on_member_join(member):
    if not db.queryMembers("_id", member.id):
        return db.insertMembers(member)

@bot.event
async def on_member_remove(member):
    if db.queryMembers("_id", member.id):
        db.removeMember("_id", member.id)

bot.run(TOKEN)