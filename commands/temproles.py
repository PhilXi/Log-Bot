import discord
import json
from discord import message
from discord import channel
from discord.ext import commands
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw
from discord.ext.commands import Cog
import asyncio


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
client = discord.Client()

class TempRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.bot.remove_command('help')


    @commands.command(pass_context=True)
    async def time(self, ctx):
        #Zeigt die Zeit an, die der User noch verfügbar ist

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                await ctx.send(f"Du hast noch {calender_data[user_id]} Minuten verfügbar.")
            else:
                await ctx.send("Du hast noch keine Zeit verfügbar.")     

    @commands.command(pass_context=True)
    async def reset(self, ctx):
        #Setzt die Zeit zurück

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                calender_data[user_id] = 00
                with open('.\\databases\\time.json', 'w') as reset_user_data:
                    json.dump(calender_data, reset_user_data, indent=4)
                await ctx.send("Du hast deine Zeit zurückgesetzt.")
            else:
                await ctx.send("Du hast noch keine Zeit verfügbar.")

    @commands.command(pass_context=True)
    async def addminutes(self, ctx, minutes: int):
        #Fügt Minuten zu deiner verfügbaren Zeit hinzu

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                calender_data[user_id] += minutes
                with open('.\\databases\\time.json', 'w') as add_minutes_user_data:
                    json.dump(calender_data, add_minutes_user_data, indent=4)
                await ctx.send(f"Du hast {calender_data[user_id]} Minuten verfügbar.")
            else:
                await ctx.send("Du hast noch keine Zeit verfügbar.")

    @commands.command(pass_context=True)
    async def removeminutes(self, ctx, minutes: int):
        #Entfernt Minuten von deiner verfügbaren Zeit

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                calender_data[user_id] -= minutes
                with open('.\\databases\\time.json', 'w') as remove_minutes_user_data:
                    json.dump(calender_data, remove_minutes_user_data, indent=4)
                await ctx.send(f"Du hast {calender_data[user_id]} Minuten verfügbar.")
            else:
                await ctx.send("Du hast noch keine Zeit verfügbar.")

    @commands.command(pass_context=True)
    async def deleteuser(self, ctx):
        #Löscht den User aus der Datenbank

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                del calender_data[user_id]
                with open('.\\databases\\time.json', 'w') as delete_user_data:
                    json.dump(calender_data, delete_user_data, indent=4)
                await ctx.send("Du hast deine Zeit gelöscht.")
            else:
                await ctx.send("Du hast noch keine Zeit verfügbar.")
            
            

    @commands.command(pass_context=True)
    async def showtimeofanotheruser(self, ctx, user: discord.Member):
        #Zeigt die verfügbare Zeit eines anderen Users an

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(user.id)

            if user_id in calender_data:
                await ctx.send(f"Der User {user.name} hat noch {calender_data[user_id]} Minuten verfügbar.")
            else:
                await ctx.send("Der User hat noch keine Zeit verfügbar.")


    
 
    @commands.command(pass_context=True)
    async def roles(self, ctx):

        guild_id = ctx.message.guild.id

        embed = discord.Embed(
            title = 'Temproles:',
            description = 'Hier könnt ihr euch eure temporären Rollen abholen.',
            colour = discord.Colour.green()
        )

        embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')
        embed.add_field(name='\u200b', value='Folgende Rollen gibt es: \n - **30** Für eine Verfügbarkeit von 30 Minuten \n - **60** Für eine Verfügbarkeit von 60 Minuten \n - **90** Für eine Verfügbarkeit von 90 Minuten', inline=False)
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:30:899420488525299742>')
        await msg.add_reaction('<:60:906324383432314910>')
        await msg.add_reaction('<:90:906327588589420544>')
        await msg.add_reaction('⛔')




    @commands.command(pass_context= True)
    async def test(self, ctx):
        
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
                user_rank_column.append([rank_index + 1])

            # User names
            for name_index, name_value in enumerate(new_timeboard[:1]):
                user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])
            
            # User Time count
            for time_count_index, time_count_value in enumerate(new_timeboard[:10]):
                user_time_column.append([time_count_value[1]])

            # Add column to table
            user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='left')
            user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Verfügbar:\n'], numalign='left')
            user_time_count_table = tabulate(user_time_column, tablefmt='plain', headers=['Verfügbar bis:\n'], numalign='left')

            # Image
            image_template = Image.open('.\\assets\\test.png')

            # Set Font
            font = ImageFont.truetype('theboldfont.ttf', 14)

            # Set the positions
            rank_text_position = 30, 50 
            name_text_position = 80, 50
            time_count_text_position = 300, 50

            # Draw
            draw_on_image = ImageDraw.Draw(image_template)
            draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
            draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
            draw_on_image.text(time_count_text_position, user_time_count_table, 'white', font=font)

            # Save the image
            image_template.convert('RGB').save('test.png', 'PNG')



            await ctx.send(file=discord.File('test.png'))


        


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        ourMessageID = 907760467487903775

        if ourMessageID == payload.message_id:
            member = payload.member
            emoji = payload.emoji.name
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            
            if emoji == '60':
                role = discord.utils.get(guild.roles, name="Verfügbar")

            if member is not None:
                await member.remove_roles(role, reason="Reaction role.")
            else:
                print("Member not found")

            
            with open('.\\databases\\time.json', 'r') as file:
                calender_data = json.load(file)
                new_user = str(member.id)

                # delete user in database
                if new_user in calender_data:
                    del calender_data[new_user]
                    with open('.\\databases\\time.json', 'w') as remove_user_data:
                        json.dump(calender_data, remove_user_data, indent=4)
                        await member.send("Du hast deine Verfügbarkeit beendet.")

                else: 
                    await member.send("Du bist nicht verfügbar.")
            
                        
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
                user_rank_column.append([rank_index + 1])

            # User names
            for name_index, name_value in enumerate(new_timeboard[:1]):
                user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])
            
            # User Time count
            for time_count_index, time_count_value in enumerate(new_timeboard[:10]):
                user_time_column.append([time_count_value[1]])

            # Add column to table
            user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='left')
            user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Verfügbar:\n'], numalign='left')
            user_time_count_table = tabulate(user_time_column, tablefmt='plain', headers=['Verfügbar für:\n'], numalign='left')

            # Image
            image_template = Image.open('.\\assets\\test.png')

            # Set Font
            font = ImageFont.truetype('theboldfont.ttf', 14)

            # Set the positions
            rank_text_position = 30, 50 
            name_text_position = 80, 50
            time_count_text_position = 300, 50

            # Draw
            draw_on_image = ImageDraw.Draw(image_template)
            draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
            draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
            draw_on_image.text(time_count_text_position, user_time_count_table, 'white', font=font)

            # Save the image
            image_template.convert('RGB').save('test.png', 'PNG')



            #send message
            await member.send(file=discord.File('test.png'))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        ourMessageID = 907760467487903775

        if ourMessageID == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name
            channel = payload.channel_id
            

            #checks what emote is added
            
            if emoji == '30':
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)
                # get channel with ourMessageID
                channel = await self.bot.fetch_channel(channel)
                # send message to channel with who is available and how long
                await channel.send(f"{member.mention} ist jetzt verfügbar für 30 Minuten")

                
                with open('.\\databases\\time.json', 'r') as file:
                    calender_data = json.load(file)
                    new_user = str(member.id)
                            
                    if new_user in calender_data:
                        calender_data[new_user] + 30
                        with open('.\\databases\\time.json', 'w') as update_user_data:
                            json.dump(calender_data, update_user_data, indent=4)

                    # add new user
                    else:
                        calender_data[new_user] = 30
                        with open('.\\databases\\time.json', 'w') as new_user_data:
                            json.dump(calender_data, new_user_data, indent=4)

                with open('.\\databases\\time.json', 'r') as file:
                    calender_data = json.load(file)
                    user_ids = list(calender_data.keys())
                    user_time_count = list(calender_data.values())

                    new_timeboard = []
                    for index, user_id in enumerate(user_ids, 1):
                        new_timeboard.append([user_id, user_time_count[index - 1]])

                    # Sort timeboard order by user time count
                    new_timeboard.sort(key=lambda items: items[1], reverse=True)

                    user_rank_column = []
                    user_name_column = []
                    user_time_column = []

                    # User ranks
                    for rank_index, rank_value in enumerate(new_timeboard[:10]):
                        user_rank_column.append([rank_index + 1])

                    # User names
                    for name_index, name_value in enumerate(new_timeboard[:10]):
                        user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])

                    # User Time count
                    for time_count_index, time_count_value in enumerate(new_timeboard[:10]):
                        user_time_column.append([time_count_value[1]])

                    # Add column to table
                    user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='left')
                    user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Verfügbar:\n'], numalign='left')
                    user_time_count_table = tabulate(user_time_column, tablefmt='plain', headers=['Verfügbar für:\n'], numalign='left')

                    # Image
                    image_template = Image.open('.\\assets\\test.png')

                    # Set Font
                    font = ImageFont.truetype('theboldfont.ttf', 14)

                    # Set the positions
                    rank_text_position = 30, 50 
                    name_text_position = 80, 50
                    time_count_text_position = 300, 50

                    # Draw
                    draw_on_image = ImageDraw.Draw(image_template)
                    draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
                    draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
                    draw_on_image.text(time_count_text_position, user_time_count_table, 'white', font=font)
                    
                    # Save the image
                    image_template.convert('RGB').save('test.png', 'PNG')
                    
                    await payload.member.send(file=discord.File('test.png'))

        


            elif emoji == '60':
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)

            elif emoji == '90':
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)


            elif emoji == '⛔':
                #delete user from database
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.remove_roles(role, reason="Reaction role.")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
                                                                
            ourMessageID = 907760467487903775
    
            if ourMessageID == payload.message_id:
                member = payload.member
                emoji = payload.emoji.name
                guild = await self.bot.fetch_guild(payload.guild_id)
                member = await guild.fetch_member(payload.user_id)
    
                if emoji == '30':
                    role = discord.utils.get(guild.roles, name="Verfügbar")
    
                    await member.remove_roles(role, reason="Reaction role.")

                    # get channel with ourMessageID
                    channel = await self.bot.fetch_channel(payload.channel_id)
                    # send message to channel 
                    await channel.send(f"{member.mention} ist jetzt nicht mehr verfügbar.")
                    
                    with open('.\\databases\\time.json', 'r') as file:
                        calender_data = json.load(file)
                        new_user = str(member.id)
                        
                        # delete user in database
                        if new_user in calender_data:
                            del calender_data[new_user]
                            
                            with open('.\\databases\\time.json', 'w') as remove_user_data:
                                json.dump(calender_data, remove_user_data, indent=4)

                        
                        
                elif emoji == '60':
                    role = discord.utils.get(guild.roles, name="Verfügbar")

                    await member.add_roles(role)
                    
                elif emoji == '90':
                    role = discord.utils.get(guild.roles, name="Verfügbar")

                    await member.add_roles(role)



        

def setup(bot):
    bot.add_cog(TempRoles(bot))