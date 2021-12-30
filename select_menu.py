import discord
from discord.ext import commands


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
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

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Choose the time you want wo be availabel",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f"You are now availabel for {self.values[0]} Minutes")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


bot = Bot()


@bot.command()
async def rolesv8(ctx):

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    embed = discord.Embed(
        title = "Temproles:",
        description = "Hier könnt ihr euch eure temporären Rollen hinzufügen.",
        colour = discord.Colour.green()
    )
    embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n - **30** Für eine Verfügbarkeit von 30 Minuten \n - **60** Für eine Verfügbarkeit von 60 Minuten \n - **90** Für eine Verfügbarkeit von 90 Minuten', inline=False)
        
    await ctx.send(embed=embed, view=view)


bot.run("")
