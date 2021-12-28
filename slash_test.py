import discord
from discord.ui import Button, View
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
    button1 = Button(label = "Hello World!", style = discord.ButtonStyle.green, emoji = "🤖") #green button
    button1_1 = Button(label = "Hello World", style = discord.ButtonStyle.blurple) # blue button
    button2 = Button(emoji = "<:members:871691185721331762>") # without any stile the default color gray is used
    button3 = Button(label = "This is a important Button", style = discord.ButtonStyle.red) 
    button4 = Button(label = "This is a Link-Button", url = "https://discord.com/")
    # add the Buttons to the message
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button1_1)
    #view.remove_item(button)
    await ctx.send(embed=discord.Embed(title="Hello World!", description="This is a test embed."), view=view)



@bot.command()
async def test(ctx):
    button = Button(label = "Hello World!", style = discord.ButtonStyle.green, emoji = "<:members:871691185721331762>") 
    async def button_callback(interaction):
        await interaction.response.send_message("Hello World!")
    button.callback = button_callback
    view = View()
    view.add_item(button)
    await ctx.send("Button", view=view)


bot.run("")