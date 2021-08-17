from typing import List
import discord
from datetime import datetime
from discord import Embed
from discord.embeds import EmptyEmbed
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
			embed.set_author(name=f"{after.nick}#{after.discriminator}",
			icon_url=after.avatar_url)
			embed.set_thumbnail(url=after.avatar_url)
			embed.set_footer(text=f"User ID: {after.id}")

			fields = [("Before", before.display_name, False),
					  ("After", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

		elif before.roles != after.roles:

			# Removes @everyone role
			roles = before.roles
			roles2 = []
			for r in roles:
				if r.name != "@everyone":
					roles2.append(r.mention)
			print(f"Before;raw {roles2}")
			# If the roles are None
			txt2 = ""
			if not roles2:
				print("list is empty")
				txt2 += "-"
			else:
				print("list not empty")
				txt2 = roles2
			# Improves the list
			txt4 = ""
			for i in txt2:
				txt4 += f"|{i} \n"
			print(f"Before: {txt4}")

			# Removes @everyone role
			roles = after.roles
			roles3 = []
			for r in roles: 
				if r.name != "@everyone":
					roles3.append(r.mention)
			# If the roles are None
			print(f"Afer;raw {roles3}")
			txt3 = ""
			if not roles3:
				print("list is empty")
				txt3 += "-"
			else:
				print("list not empty")
				txt3 = roles3
			# Improves the list
			txt5 = ""
			for i in txt3:
				txt5 += f"|{i} \n"
			print(f"After: {txt5}")
		

			embed = Embed(
				colour = discord.Colour.blue(),
				description=f"{after.mention}'s Rollen haben sich aktualisiert:",
				timestamp = datetime.utcnow()
			)
			embed.set_author(name=f"{after.name}#{after.discriminator}",
			icon_url=after.avatar_url)
			embed.set_thumbnail(url=after.avatar_url)
			embed.add_field(name='Before:', value=f"{txt4}", inline=True)
			embed.add_field(name='After:', value=f"{txt5}", inline=True)
			embed.set_footer(text=f"User ID: {after.id}"),

			await self.log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(ServerProfileChanges(bot))