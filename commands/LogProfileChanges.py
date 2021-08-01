import discord
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


class ProfileChanges(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
			self.log_channel = self.bot.get_channel(870282114510233690)
	
	Cog.listener()
	async def on_user_update(self, before, after):

		# Loggs changes to the Username
		if before.name != after.name:

			embed = Embed(
				colour = discord.Colour.purple(),
				description=f"{after.mention} hat seinen Profil-Namen aktualisiert:",
				timestamp = datetime.utcnow()
            )
			embed.set_author(name=after.name,
			icon_url=after.avatar_url)
			embed.set_thumbnail(url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			fields = [("Before", before.name, False),("After", after.name, False)]
			
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)


		# Loggs changes to the Discriminator of a User
		elif before.discriminaotr != after.discriminator:
			embed = Embed(
				colour = discord.Colour.purple(),
				description=f"{after.mention} hat seinen Diskriminator aktualisiert:",
				timestamp = datetime.utcnow()
            )
			embed.set_author(name=after.name,
			icon_url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			fields = [("Before", before.discriminator, False),("After", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
				
			await self.log_channel.send(embed=embed)

		# Loggs changes to the Profilepicture of a User
		elif before.avatar_url != after.avatar_url:
			embed = Embed(
				colour = discord.Colour.purple(),
				description=f"{after.mention} hat sein Profilbild aktualisiert:",
				timestamp = datetime.utcnow()
            )
			embed.set_author(name=after.name,
			icon_url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)

			await self.log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(ProfileChanges(bot))