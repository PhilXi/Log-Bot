import discord
import json
from discord import message
from discord.ext import commands
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

class TempRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        ourMessageID = 899754595566354492

        if ourMessageID == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name         

            if emoji == '30':
                role = discord.utils.get(guild.roles, name="Verfügbar")

            await member.add_roles(role)

            with open('.\\databases\\test.json', 'r') as file:
                calender_data = json.load(file)
                new_user = str(member)

                # remove old user
                if new_user in calender_data:
                    calender_data[new_user] -= 1
                    with open('.\\databases\\time.json', 'w') as remove_user_data:
                        json.dump(calender_data, remove_user_data, indent=4)

                elif new_user in calender_data:
                    calender_data[new_user] +=1
                    with open('.\\databases\\time.json', 'w') as update_user_data:
                        json.dump(calender_data, update_user_data, indent=4)

                # add new user
                else:
                    calender_data[new_user] = 1
                    with open('.\\databases\\time.json', 'w') as new_user_data:
                        json.dump(calender_data, new_user_data, indent=4)

            
            with open('.\\databases\\time.json', 'r') as file:
                calender_data = json.load(file)
            
            user_ids = list(calender_data.keys())
            user_time_count = list(calender_data.values())

            new_timeboard = []

            for index, user_ids in enumerate(user_ids, 1):
                new_timeboard.append([user_ids, user_time_count])

            # Sort timeboard order by user time count
            new_timeboard.sort(key=lambda items: items[1], reverse=True)

            user_rank_column = []
            user_name_column = []
            user_time_column = []

            # User ranks
            for rank_index, rank_value in enumerate(new_timeboard[:10]):
                user_name_column.append([rank_index + 1])

            # User names
            for name_index, name_value in enumerate(new_timeboard[:10]):
                user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])
            
            # User Time count
            for time_count_index, time_count_value in enumerate(new_timeboard[:10]):
                user_time_column.append([time_count_value[1]])

            # Add column to table
            user_rank_table = tabulate
            user_name_table = tabulate
            user_time_count_table = tabulate


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        ourMessageID = 899754595566354492

        if ourMessageID == payload.message_id:
            emoji = payload.emoji.name
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            
            if emoji == '30':
                role = discord.utils.get(guild.roles, name="Verfügbar")

            if member is not None:
                await member.remove_roles(role, reason="Reaction role.")
            else:
                print("Member not found")

            
            with open('.\\databases\\test.json', 'r') as file:
                calender_data = json.load(file)
                new_user = str(member)

                # remove old user
                if new_user in calender_data:
                    calender_data[new_user] -= 1
                    with open('.\\databases\\time.json', 'w') as remove_user_data:
                        json.dump(calender_data, remove_user_data, indent=4)
                
                
                elif new_user in calender_data:
                    calender_data[new_user] +=1
                    with open('.\\databases\\time.json', 'w') as update_user_data:
                        json.dump(calender_data, update_user_data, indent=4)


                # add new user
                else:
                    calender_data[new_user] = 1
                    with open('.\\databases\\time.json', 'w') as new_user_data:
                        json.dump(calender_data, new_user_data, indent=4)

            
            

    
 
    @commands.command(pass_context=True)
    async def roles(self, ctx):

        guild_id = ctx.message.guild.id

        embed = discord.Embed(
            title = 'Temproles:',
            description = 'Hier könnt ihr euch eure temporären Rollen abholen.',
            colour = discord.Colour.green()
        )

        embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')
        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n - <:30:899420488525299742> Für eine Verfügbarkeit von 30 Minuten', inline=False)
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:30:899420488525299742>')

    


def setup(bot):
    bot.add_cog(TempRoles(bot))