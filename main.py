# Manual file imports
import asyncio
import datetime
import json
from uuid import uuid4

# Logging format
import logging
import platform
import time

from discord.utils import get
import discord
import requests
from colorama import init
from discord.ext import commands
from discord.ext.tasks import loop
from termcolor import colored

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

import config as CONFIG  # Capitals for global
import embeds as EMBEDS  # Capitals for global
import gsheet as GSHEET  # Capital for global


class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def warning(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'{message}', "blue"))


logger = Logger("kourage")

# FOR TESTING
# bot = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.members = True

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))

@bot.event
async def on_member_join(member):  # Triggers when members joins the server
    #await member.send('Thank you for joining Koders') # Have an embed there
    role = get(member.guild.roles, id=726643908624515195)
    await member.add_roles(role)
    

# TODO
# Add Duckhunt system responsive
# Look for setting career at koders with something better at server setup
# Google doc requirement on Koders App
# Sprint showcase

# Attendance System
def check(reaction, user):
    return str(reaction.emoji) == '⬆️' and user.bot is not True


async def take_reaction(ctx, timeout=1200.0):
    start = time.time()
    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.delete()
    else:
        reaction, user = result
        channel = await user.create_dm()
        date_time = datetime.datetime.now()
        embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
        await channel.send(embed=embed)
        end = time.time()
        timeout = timeout - (end - start)
        logger.warning(user)

        # Write into Gsheet Username Time Date
        GSHEET.insert(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), user)
        logger.warning(user)
        await take_reaction(ctx, timeout=timeout)


async def take_attendance_morning(ctx):
    embed = EMBEDS.attendance("11:00", "11:20")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    await take_reaction(msg)


async def take_attendance_lunch(ctx):
    embed = EMBEDS.attendance("3:00", "3:20")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    await take_reaction(msg)


@loop(minutes=1)
async def attendance_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(839125549304643684)  # attendance channel id
    working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    date_time = datetime.datetime.now()
    for working_day in working_days:
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "11:00":
            logger.info("Ran morning attendance.")
            await take_attendance_morning(channel)
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "15:00":
            logger.info("Ran post lunch attendance.")
            await take_attendance_lunch(channel)
    logger.info("Waiting for tasks...")


# Ping command
@bot.command()
@commands.has_any_role("@everyone")
async def ping(msg):
    await msg.send('Pong! 🏓\n ' +
                'Name: Kourage \n ' +
                'Description: AIO bot of Koders \n ' +
                'Version: {0} \n '.format(CONFIG.VERSION) +
                'Username: {0} \n '.format(msg.author.name) +
                'Latency: {0} sec '.format(round(bot.latency, 1)))


# Define command
@bot.command()
@commands.has_any_role("Koders")
async def define(msg, *args):
    response = None
    word = args[0]  # API REQUEST
    url = 'https://owlbot.info/api/v4/dictionary/' + str(word)
    headers = {"Authorization": CONFIG.OWL_TOKEN}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        logger.error("Something went wrong during requesting API. Reason: " + str(e))  # Request exception

    data = json.loads(response.text)  # JSON PARSE WITH EMBED
    try:
        for i in range(0, len(data['definitions'])):
            embed = discord.Embed(title="Word: " + str(word), color=0x57b28f)
            embed.set_author(name="Kourage Word Analyzer",
                            url="https://www.github.com/koders-in/kourage",
                            icon_url=bot.user.avatar_url)
            if data['definitions'][i]['image_url'] is not None:
                embed.set_thumbnail(url=data['definitions'][i]['image_url'])
            embed.add_field(name="Type",
                            value=data['definitions'][i]['type'],
                            inline=True)
            embed.add_field(name="Meaning",
                            value="**" + data['definitions'][i]['definition'] + "**",
                            inline=False)
            if data['definitions'][i]['example'] is None:
                data['definitions'][i]['example'] = "N/A"
            embed.add_field(name="Example",
                            value="_" + data['definitions'][i]['example'] + "_",
                            inline=False)
            embed.set_footer(text="Made with ❤️️  by Koders")
            await msg.send(embed=embed)
    except Exception as e:
        Logger.error("Something went wrong during parsing JSON. Reason: " + str(e))  # JSON parsing exception
        await msg.send("Can't find its meaning over the database")  # Sending message so user can read


# Vision command
@bot.command()
@commands.has_any_role("Kore")
async def vision(msg):
    await msg.message.delete()
    embed = EMBEDS.vision()
    await msg.send(embed=embed)


# Suggestion command
@bot.command()
@commands.has_any_role("Koders")
async def suggestion(ctx):
    emojis = ['✅','❌'] 
    channel = bot.get_channel(849583285645475850)
    suggestEmbed = discord.Embed(colour=0x28da5b)
    suggestEmbed=discord.Embed(title="Suggestion Bot", description="To accept the suggestion: ✅"
                                                                    "To decline the suggestion: ❌", color=0x28da5b)
    suggestEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed.timestamp = datetime.datetime.utcnow()
    suggestEmbed.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed.set_author(name = f'suggested by {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    
    # Title
    suggestEmbed1 = discord.Embed(colour=0x28da5b)
    suggestEmbed1 = discord.Embed(
        title = 'Please tell me the title of the Suggestion',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed = suggestEmbed1)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )
        
        if msg:
            await sent.delete()
            titlemessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 10)
        
        
    # description
    suggestEmbed2 = discord.Embed(colour=0x28da5b)
    suggestEmbed2 = discord.Embed(
        title = 'Please tell me the Description of the Suggestion',
        description = ' This request will timeout after 5 minutes'
    )
    sent2 = await ctx.send(embed = suggestEmbed2)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )
        
        if msg:
            await sent2.delete()
            descriptionmessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent2.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300.0)
        
    # Unique ID
    eventid = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    uniqueID = eventid[48:].upper()
    
    suggestEmbed.add_field(name='Ticket ID: ', value = f'{uniqueID}', inline=False)    
    suggestEmbed.add_field(name = 'Title', value  = f'{titlemessage}',inline = False)
    suggestEmbed.add_field(name = 'Description', value  = f'{descriptionmessage}',inline = False)
    
    
    message = await channel.send(embed = suggestEmbed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    
    sendEmbed = discord.Embed(colour = 0x28da5b)
    # sendEmbed.add_field(name = 'New Suggestion!', value  = f'{suggestion}')
    sendEmbed.add_field(name = 'Title', value  = f'{titlemessage}')
    sendEmbed.add_field(name = 'Description', value  = f'{descriptionmessage}')
    sendEmbed.add_field(name='Ticket ID: ', value = f'{uniqueID}', inline=False) 
    sendEmbed.set_author(name = f'suggested by {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.timestamp = datetime.datetime.utcnow()
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    
    def check (reaction, user):
        return not user.bot and message == reaction.message
    
    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run because of like 31,32
        while reaction.message == message:
            if str(reaction.emoji) == "✅":
                # Role logic
                xstring = ''
                for role in user.roles:
                    if(role.name == '@everyone'):
                        continue
                    else:
                        xstring += role.name
                        xstring += ','
                xstring = xstring[:-1]
                
                await ctx.send(f'🙌🙌 Bravo!! Your suggestion has been Acknowledged by {user} who has these roles ({xstring}). We appreciate your efforts!')
                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                await channel.send(f'suggestion of {ctx.message.author}, with ID: {uniqueID} has been approved by {user} who has these roles ({xstring}), this post will no longer be active')
                return
            if str(reaction.emoji) == "❌":
                
                # Role logic
                xstring = ''
                for role in user.roles:
                    if(role.name == '@everyone'):
                        continue
                    else:
                        xstring += role.name
                        xstring += ' '
                xstring = xstring[:-1]
                await ctx.send(f'🌸 Sorry! Your suggestion has not been Acknowledged by {user} who has these roles ({xstring}). We thank you for your valuable time!')
                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                await channel.send(f'suggestion of {ctx.message.author}, with ID: {uniqueID} has not been approved by {user} who has these roles ({xstring}), this post will no longer be active')
                return
    except asyncio.TimeoutError:
        await ctx.send("Your suggestion was timed out. Please try again!")
        return


# Remind command
@bot.command()
@commands.has_any_role("Koders")
async def remind(msg, *args):
    await msg.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    embed = discord.Embed(title="Hello there! You have a reminder ^_^",
                        color=0x57b28f)
    embed.add_field(name="Don't forget to:",
                    value="{0}".format(args[1]),
                    inline=False)
    embed.add_field(name="By yours truly :ghost:",
                    value="Kourage",
                    inline=False)
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2919/2919780.svg")
    embed.set_footer(text="Made with ❤️️  by Koders")
    await msg.send(embed=embed)
    if len(args) > 2:
        msg = await msg.send(args[2])
        await msg.delete()  # Deletes @person message who got tagged


# Poll command
@bot.command()
@commands.has_any_role('Koders')
async def poll(msg, question, *options: str):
    await msg.message.delete()
    embed = discord.Embed(title="Hello there! Please vote. ^_^",
                        description=question,
                        color=0x54ab8a)
    embed.set_author(name="Koders")
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    for _x, option in enumerate(options):
        embed.add_field(name=reactions[_x],
                        value=option,
                        inline=True)
    embed.set_footer(text="Made with ❤️️  by Koders")
    react_message = await msg.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)
        



if __name__ == "__main__":
    try:
        attendance_task.start()
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
