import discord
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
			self.log_channel = self.bot.get_channel(870282114510233690)
			self.bot.cogs_ready.ready_up("log")

	@Cog.listener()
	async def on_message_edit(self, before, after):
		#if not after.author.bot:
			if before.content != after.content:
				embed = Embed(

					title="Message edit",
					description=f"Edit by {after.author.display_name}.",
					colour = discord.Colour.orange(),
					timestamp=datetime.utcnow()
				)

				fields = [("Before", before.content, False),
						  ("After", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		#if not message.author.bot:
			embed = Embed(

                title=f"Message deletion",
				description=f"Action by {message.author.display_name}.",
				colour = discord.Colour.red(),
				timestamp=datetime.utcnow()
            )

			fields = [("Content", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Log(bot))