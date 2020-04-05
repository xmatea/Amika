import discord
from discord.ext import commands
from datetime import date, datetime
from dotenv import load_dotenv
import os
import logging
import utils.process as process
import utils.database as db

logging.basicConfig(level=logging.INFO)
load_dotenv()
TOKEN = os.getenv("TOKEN")

Config = process.readjson('config.json')

class Amika(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None)
        self.command_prefix = Config.prefix

bot = Amika()

# read and loag cogs
for file in os.listdir("cogs"):
    if file.endswith('.py'):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        

@bot.event
async def on_ready():
    print("Amika started at {0}, loaded {1} cog(s)".format(datetime.now().strftime("%H:%M:%S"), len(bot.cogs)))

@bot.event
async def on_guild_join(guild):
    db.insert_guild(guild)

    for member in guild.members:
        if(member != bot.user):
            db.insert_member(member)

bot.run(TOKEN)