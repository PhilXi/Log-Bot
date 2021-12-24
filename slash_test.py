import discord
from discord.ui import Button, View
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
    button = Button(label="Hello World!", style=discord.ButtonStyle.green, emoji="🤖")
    view = View()
    view.add_item(button)
    await ctx.send(embed=discord.Embed(title="Hello World!", description="This is a test embed."), view=view)


bot.run("")