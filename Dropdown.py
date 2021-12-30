import discord
from discord.ext import commands

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(
                label="30 Minutes"
            ),
            discord.SelectOption(
                label="60 Minutes"
            ),
            discord.SelectOption(
                label="90 Minutes"
            ),
            discord.SelectOption(
                label="Reset", emoji="⛔"
            )
        ]
        # the placeholder will be shown when noch option is chosen
        super().__init__(
            placeholder="Choose the time you want wo be availabel",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You are now availabel for {self.values[0]} Minutes")
