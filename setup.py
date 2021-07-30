import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands

class LogBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Connect
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} ({self.bot.user.id})')

    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')
        
    # Error Handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)
    

# Gateway intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Bot prefix
bot = commands.Bot(command_prefix='!',description='Log Bot', intents=intents, case_insensitive=True)
bot.remove_command("help")

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Loading data from .env file
load_dotenv()
token = os.getenv('TOKEN')

if __name__ == '__main__':
    #load extention
    for filename in os.listdir('.\\commands'):
        if filename.endswith('.py'):
           bot.load_extension(f'commands.{filename[: -3]}')

    bot.add_cog(LogBot(bot))
    bot.run(token, reconnect=True)