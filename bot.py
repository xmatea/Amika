import discord
from discord.ext import commands
from datetime import datetime

from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("TOKEN")

import logging
logging.basicConfig(level=logging.INFO)

import utils.process as process
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

bot.run(TOKEN)