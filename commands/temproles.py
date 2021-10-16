import discord
import json
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

class TempRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        ourMessageID = 899030790644584469

        if ourMessageID == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name         

            if emoji == '1️⃣':
                role = discord.utils.get(guild.roles, name="Verfügbar")

            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        ourMessageID = 899030790644584469

        if ourMessageID == payload.message_id:
            emoji = payload.emoji.name
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            
            if emoji == '1️⃣':
                role = discord.utils.get(guild.roles, name="Verfügbar")

            if member is not None:
                await member.remove_roles(role, reason="Reaction role.")
            else:
                print("Member not found")

    
 
    @commands.command(pass_context=True)
    async def roles(self, ctx):

        guild_id = ctx.message.guild.id

        embed = discord.Embed(
            title = 'Temproles:',
            description = 'Hier könnt ihr euch eure temporären Rollen abholen.',
            colour = discord.Colour.green()
        )

        embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')
        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n \n - <:YouTube:864980517630902302> Youtube: Dann erhaltet ihr einen Ping, wenn ein YouTube-video hochgeladen wurde. \n \n - <:Twitch:864980843176787988> Twitch: Ihr bekommt einen Ping, wenn ein Creator Live geht. \n \n - <:Discord:864980938068852757> Discord: Diese Rolle wird gepingt wenn es News zu dem Discord gibt. \n \n - <a:alert:864983948987990081> Community-Events : Ihr bekommt einen Ping wenn wir ein Event veranstalt', inline=False)
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')

    


def setup(bot):
    bot.add_cog(TempRoles(bot))