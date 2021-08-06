import discord
from discord import channel
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        MessageID = 872591529921888327

        if MessageID == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name         

            if emoji == 'members':
                role = discord.utils.get(guild.roles, name="Mitglied")

            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        MessageID = 872591529921888327

        if MessageID == payload.message_id:
            emoji = payload.emoji.name
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            
            if emoji == 'members':
                role = discord.utils.get(guild.roles, name="Mitglied")

            if member is not None:
                await member.remove_roles(role, reason="Reaction role.")
            else:
                print("Member not found")

    @commands.command(pass_context=True)
    async def role(self, ctx):

        guild_id = ctx.message.guild.id

        embed = discord.Embed(
            title = 'Reactionroles',
            description = 'Hey, hier könnt ihr euch eure Rollen abholen.',
            colour = discord.Colour.green()
        )

        embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')
        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n \n - <:members:871691185721331762> Mitglied: (...)', inline=False)
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:members:871691185721331762>')


def setup(bot):
    bot.add_cog(ReactionRoles(bot))