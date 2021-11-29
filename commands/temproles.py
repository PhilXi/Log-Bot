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
                await ctx.send("Du hast keine Zeit mehr verfügbar.")     

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

        # turn every minute into 60 seconds
        minutes = minutes * 60
        

        with open('.\\databases\\time.json', 'r') as file:
            calender_data = json.load(file)
            user_id = str(ctx.message.author.id)

            if user_id in calender_data:
                calender_data[user_id] += minutes
                with open('.\\databases\\time.json', 'w') as add_minutes_user_data:
                    json.dump(calender_data, add_minutes_user_data, indent=4)
                    # turn every 60 seconds into minutes
                await ctx.send(f"Du hast {calender_data[user_id] / 60} Minuten verfügbar.")
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
        await msg.add_reaction('<:30:912465249716809729>')
        await msg.add_reaction('<:60:912460146779775028>')
        await msg.add_reaction('<:90:912459869976657920>')
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
            image_template = Image.open('.\\assets\\time.png')

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


            # turn every 60 seconds into minutes



            draw_on_image.text(time_count_text_position, (f'{user_time_count / 60} Minuten'), 'white', font=font)

            # Save the image
            image_template.convert('RGB').save('time.png', 'PNG')



            await ctx.send(file=discord.File('time.png'))



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        ourMessageID = 913933850739097610


        if ourMessageID == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name
            channel = payload.channel_id
            message = await guild.get_channel(channel).fetch_message(ourMessageID)

            #checks which emote is added

            if emoji == '30':
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)
                # get channel with ourMessageID
                channel = await self.bot.fetch_channel(channel)
                                

                # get the emote that had been added
                emote = discord.utils.get(message.guild.emojis, name="30")
                # get the member who reacted
                member1 = message.guild.get_member(payload.user_id)
                # remove the emote from the message
                await message.remove_reaction(emote, member1)


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
                    image_template = Image.open('.\\assets\\time.png')

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
                    draw_on_image.text(time_count_text_position, (f'{user_time_count_table} Minuten'), 'white', font=font)
                    
                    # Save the image
                    image_template.convert('RGB').save('time.png', 'PNG')
                    
                    await payload.member.send(file=discord.File('time.png'))
  
                # send message to channel with who is available and how long
                await channel.send(f"{member.mention} ist jetzt verfügbar für 30 Minuten")

                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

                
                # remove role after 30 minutes
                await asyncio.sleep(15)
                # check if minutes are zero
                if calender_data[new_user] == 0:
                    await member.remove_roles(role)
                else:
                    return
                # send message to channel that the user is no longer available
                await channel.send(f"{member.mention} ist nicht mehr verfügbar")

                
                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

            elif emoji == '60':
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)
                # get channel with ourMessageID
                channel = await self.bot.fetch_channel(channel)

                # get the emote that had been added
                emote = discord.utils.get(message.guild.emojis, name="60")

                # get the member who reacted
                member2 = message.guild.get_member(payload.user_id)

                # remove the emote from the message
                await message.remove_reaction(emote, member2)
                    

                with open('.\\databases\\time.json', 'r') as file:
                    calender_data = json.load(file)
                    new_user = str(member.id)
                            
                    if new_user in calender_data:
                        calender_data[new_user] + 60
                        with open('.\\databases\\time.json', 'w') as update_user_data:
                            json.dump(calender_data, update_user_data, indent=4)

                    # add new user
                    else:
                        calender_data[new_user] = 60
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
                    image_template = Image.open('.\\assets\\time.png')

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
                    draw_on_image.text(time_count_text_position, (f'{user_time_count_table} Minuten'), 'white', font=font)
                    
                    # Save the image
                    image_template.convert('RGB').save('time.png', 'PNG')
                    
                    await payload.member.send(file=discord.File('time.png'))

                    
                # send message to channel with who is available and how long
                await channel.send(f"{member.mention} ist jetzt verfügbar für 60 Minuten")

                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

                
                # remove role after 30 minutes
                await asyncio.sleep(3600)
                await member.remove_roles(role)
                # send message to channel that the user is no longer available
                await channel.send(f"{member.mention} ist nicht mehr verfügbar")

                
                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

            elif emoji == '90':
                
                role = discord.utils.get(guild.roles, name="Verfügbar")

                await member.add_roles(role)
                # get channel with ourMessageID
                channel = await self.bot.fetch_channel(channel)

                # get the emote that had been added
                emote = discord.utils.get(message.guild.emojis, name="90")

                # get the member who reacted
                member2 = message.guild.get_member(payload.user_id)

                # remove the emote from the message
                await message.remove_reaction(emote, member2)
                    

                with open('.\\databases\\time.json', 'r') as file:
                    calender_data = json.load(file)
                    new_user = str(member.id)
                            
                    if new_user in calender_data:
                        calender_data[new_user] + 90
                        with open('.\\databases\\time.json', 'w') as update_user_data:
                            json.dump(calender_data, update_user_data, indent=4)

                    # add new user
                    else:
                        calender_data[new_user] = 90
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
                    image_template = Image.open('.\\assets\\time.png')

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
                    draw_on_image.text(time_count_text_position, (f'{user_time_count_table} Minuten'), 'white', font=font)
                    
                    # Save the image
                    image_template.convert('RGB').save('time.png', 'PNG')
                    
                    await payload.member.send(file=discord.File('time.png'))

                    
                # send message to channel with who is available and how long
                await channel.send(f"{member.mention} ist jetzt verfügbar für 90 Minuten")

                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

                
                # remove role after 30 minutes
                await asyncio.sleep(5400)
                await member.remove_roles(role)
                # send message to channel that the user is no longer available
                await channel.send(f"{member.mention} ist nicht mehr verfügbar")

                
                # delete the message after 5 seconds
                await asyncio.sleep(5)

                # get the last message in the channel
                last_message = await channel.history(limit=1).flatten()

                # delete the message
                await last_message[0].delete()

            elif emoji == '⛔':
                role = discord.utils.get(guild.roles, name="Verfügbar")
                        
                await member.remove_roles(role, reason="Reaction role.")
                # check if user if is in time.json if so remove user from time.json
                with open('.\\databases\\time.json', 'r') as file:
                    calender_data = json.load(file)
                    new_user = str(member.id)
                            
                    if new_user in calender_data:
                        del calender_data[new_user]
                        with open('.\\databases\\time.json', 'w') as update_user_data:
                            json.dump(calender_data, update_user_data, indent=4)

                # get channel with ourMessageID
                channel = await self.bot.fetch_channel(channel)

                # shows how long user is available
                with open('.\\databases\\time.json', 'r') as file:
                    user_time_count_table = json.load(file)
                
                # sends message to channel
                await channel.send(f"{member.mention} ist jetzt nicht mehr verfügbar")

                




                # remove reaction
                await payload.message.remove_reaction(emoji, member)


        

def setup(bot):
    bot.add_cog(TempRoles(bot))