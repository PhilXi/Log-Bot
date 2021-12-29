from typing import List
import discord
from datetime import datetime, timezone
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime


class ServerJoinsLeaves(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
			self.log_channel = self.bot.get_channel(870282114510233690)

	@Cog.listener()
	async def on_member_remove(self, member):
		embed = Embed(
			colour = discord.Colour.red(),
			description=f":outbox_tray: {member.mention} hat den Server verlassen",
			timestamp = datetime.utcnow()
        )
		embed.set_author(name=f"{member.name}#{member.discriminator}",
		icon_url=member.display_avatar)
		embed.set_thumbnail(url=member.display_avatar)
		#embed.add_field(f"{member.mention} hat den Server verlassen")
		embed.set_footer(text=f"User ID: {member.id}")

		await self.log_channel.send(embed=embed)
		
	@Cog.listener()
	async def on_member_join(self, member):
		embed = Embed(
			colour = discord.Colour.green(),
			description=f":inbox_tray: {member.mention} ist dem Server beigetreten",
			timestamp = datetime.utcnow()
        )
		embed.set_author(name=f"{member.name}#{member.discriminator}",
		icon_url=member.display_avatar)
		embed.set_thumbnail(url=member.display_avatar)
		embed.add_field(name='Accounterstellung', value=member.created_at.strftime("%d.%m.%Y"), inline=False)
		embed.set_footer(text=f"User ID: {member.id}")

		await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerJoinsLeaves(bot))