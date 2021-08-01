import discord
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


class ServerProfileChanges(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
			self.log_channel = self.bot.get_channel(870282114510233690)

	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(
				colour = discord.Colour.blue(),
				description=f"{after.mention} hat seinen Server-Namen Aktualisiert:",
				timestamp = datetime.utcnow()
            )
			embed.set_author(name=after.name,
			icon_url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			fields = [("Before", before.display_name, False),
					  ("After", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

		elif before.roles != after.roles:
			embed = Embed(
				colour = discord.Colour.blue(),
				description=f"{after.mention}'s Rollen haben sich aktualisiert:",
				timestamp = datetime.utcnow()
            )
			embed.set_author(name=after.name,
			icon_url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			fields = [("Before:", ", ".join([r.mention for r in before.roles]), False),
					  ("After:", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)



def setup(bot):
	bot.add_cog(ServerProfileChanges(bot))