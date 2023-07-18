import disnake
from disnake.ext import commands
import os

from dotenv import load_dotenv
load_dotenv()

# Create a new instance of the bot
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents, activity=disnake.Activity(type=disnake.ActivityType.watching, name='the market.'), test_guilds=[1074838662879129650]) # 791818283867045941

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Load all cogs recursively
def load_cogs(bot, path):
    for file in os.listdir(path):
        if file.endswith('.py') and not file.startswith('-'):
            cog = file[:-3]
            try:
                bot.load_extension(f'cogs.{cog}')
                print(f'Loaded cog: {cog}')
            except Exception as e:
                print(f'Failed to load cog {cog}: {e}')
        elif os.path.isdir(os.path.join(path, file)):
            load_cogs(bot, os.path.join(path, file))

load_cogs(bot, 'cogs')

# Run the bot
bot.run(os.getenv('TOKEN'))

# from mongo import *

# col_stocks.update_many({}, { '$unset': { 'history': '' } })
# col_stocks.update_many({}, { '$set': { 'activity': [] } })

# col_stocks.update_one({ '_id': 'MOV' }, { '$push': { 'sell_offers': { 'cost': 100, 'quantity': 10, 'seller': 'market' } } })
# col_stocks.update_one({ '_id': 'MOV' }, { '$push': { 'sell_offers': { 'cost': 67, 'quantity': 3, 'seller': 'market' } } })
# col_stocks.update_one({ '_id': 'MOV' }, { '$push': { 'sell_offers': { 'cost': 101, 'quantity': 11, 'seller': 'market' } } })