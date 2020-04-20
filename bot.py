import discord
from discord.ext import commands
from datetime import date, datetime
from dotenv import load_dotenv
import os
import logging
import utils.process as process
from mongo import db

logging.basicConfig(level=logging.INFO)
Config = process.readjson('config.json')

load_dotenv()
TOKEN = os.getenv("TOKEN")

class Amika(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=Config.prefix)
        #self.command_prefix = Config.prefix

bot = Amika()

# read and load cogs
bot.remove_command('help')
bot.remove_cog('general')
for file in os.listdir("cogs"):
    if file.endswith('.py'):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")
        

@bot.event
async def on_ready():
    print("Amika started at {0}, loaded {1} cog(s)".format(datetime.now().strftime("%H:%M:%S"), len(bot.cogs)))

bot.run(TOKEN)