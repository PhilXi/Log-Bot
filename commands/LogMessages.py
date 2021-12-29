import discord
from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.message import Attachment


class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
			self.log_channel = self.bot.get_channel(870282114510233690)

	@Cog.listener()
	async def on_message_edit(self, before, after):
		#if not after.author.bot:
			if before.content != after.content:
				embed = Embed(

					title="Message edited",
					description=f"A [message]({after.jump_url}) from {after.author.mention} in {after.channel.mention} was edited",
					colour = discord.Colour.orange(),
					timestamp=datetime.utcnow()
				)
				embed.set_author(name=after.author,
				icon_url=after.author.avatar_url)
				embed.set_footer(text=f"User ID: {after.author.id} " + "\n" f"Message ID: {after.id}")

				fields = [("Before", before.content, False),
						  ("After", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		#if not message.author.bot:
			embed = Embed(

                title="Message deleted",
				description=f"A message from {message.author.mention} in {message.channel.mention} was deleted",
				colour = discord.Colour.red(),
				#url=message.author.display_avatar,
				timestamp=datetime.utcnow()
            )
			embed.set_author(name=message.author,
			icon_url=message.author.display_avatar)
			embed.set_footer(text=f"User ID: {message.author.id} " + "\n" f"Message ID: {message.id}")
			# checks if the message has attachments and return if so
			if message.attachments:
				await self.log_channel.send(message.attachments[0].url)
				# check if the message only has attachments
				if message.content == "":
					# define the message.content as the attachment name and hyperlink the attachment url
					message.content = f"[{message.attachments[0].filename}]({message.attachments[0].url})"


			fields = [("Content:", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Log(bot))