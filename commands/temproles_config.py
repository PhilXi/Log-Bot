import discord
from discord.commands import Option
from discord.ext.commands.bot import AutoShardedBot
from discord.ui import Button, View, view
from discord.ext import commands

# import the class DropdownView from the file DropdownView.py
from DropdownView import DropdownView

class TempRoles_Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    bot = discord.Bot(command_prefix='!')

    @commands.slash_command(name="roles", description="Selfrole-Embed", guild_ids=[869166822245670912])
    async def rolesv4(self,ctx):




        embed = discord.Embed(
            title = "Temproles:",
            description = "Hier könnt ihr euch eure temporären Rollen hinzufügen.",
            colour = discord.Colour.green()
        )

        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n - **30** Für eine Verfügbarkeit von 30 Minuten \n - **60** Für eine Verfügbarkeit von 60 Minuten \n - **90** Für eine Verfügbarkeit von 90 Minuten', inline=False)
        
        # Adds buttons instead of reactions to a message
        button30 = Button(label="30", style=discord.ButtonStyle.blurple)
        # Response to 30-Button
        async def button30_callback(interaction):
            await interaction.response.send_message("Test - 30")
        button30.callback = button30_callback
        # 60 Minutes
        button60 = Button(label='60', style=discord.ButtonStyle.blurple)
        # Response to 60-Button
        async def button60_callback(interaction):
            await interaction.response.send_message("Test - 60")
        button30.callback = button60_callback
        # 90 Minutes
        button90 = Button(label="90", style=discord.ButtonStyle.blurple)
        # Response to 90-Button
        async def button90_callback(interaction):
            await interaction.response.send_message("Test - 90")
        button30.callback = button90_callback
        # Reset the time 
        ResetButton = Button(style=discord.ButtonStyle.danger, emoji="⛔")
        # Response to Reset-Button
        async def ResetButton_callback(interaction):
            await interaction.response.send_message("Test - Reset")
        button30.callback = ResetButton_callback

        view = View()
        view.add_item(button30)
        view.add_item(button60)
        view.add_item(button90)
        view.add_item(ResetButton)

        await ctx.respond(embed=embed, view=view)

    @commands.slash_command(name="select", description="Selfrole-Embed", guild_ids=[869166822245670912])
    async def rolesv9(self,ctx):

        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        embed = discord.Embed(
            title = "Temproles:",
            description = "Hier könnt ihr euch eure temporären Rollen hinzufügen.",
            colour = discord.Colour.green()
        )
        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n - **30** Für eine Verfügbarkeit von 30 Minuten \n - **60** Für eine Verfügbarkeit von 60 Minuten \n - **90** Für eine Verfügbarkeit von 90 Minuten', inline=False)
        
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(TempRoles_Config(bot))