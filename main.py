from __future__ import print_function
import discord
from discord.ext import commands, tasks
import time
import asyncio
from datetime import datetime, date
import json
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import sqlite3
from matplotlib import pyplot as plt
import csv
import pandas as pd
	
###############################################################################################################
# MANUAL IMPORTS
###############################################################################################################
import register as REGISTER
import task as TASK
import suggestion_box as SUGGESTION_BOX
import settings as setting
import games as GAMES
import music as MUSIC
import kick_ban_unban as KICK_BAN_UNBAN
import plot_user_activity as PLOT_USER_ACTIVITY

import info
import worklogger as work
import credentials
import vision as vs

TOKEN = setting.TOKEN
client = commands.Bot(command_prefix=".")

count = 0

###############################################################################################################
# DATABASE CONNECTION
###############################################################################################################
db_file = "demo.db"
try:
	mydb = sqlite3.connect(db_file)
	mycur = mydb.cursor()
except Exception as e:
	print(e)


###############################################################################################################
# Client Table
###############################################################################################################

mycur.execute("""create table if not exists client(Id integer NOT NULL,
	Name text NOT NULL DEFAULT 'NONE',
	Address text NOT NULL DEFAULT 'NONE',
	Gender text NOT NULL DEFAULT 'NONE', 
	DOB text NOT NULL DEFAULT 'NONE',
	Discord_Username text NOT NULL DEFAULT 'NONE',
	Mail text NOT NULL DEFAULT 'NONE',
	Phone text NOT NULL DEFAULT 'NONE',
	Whatsapp text NOT NULL DEFAULT 'NONE',
	Notes text NOT NULL DEFAULT 'NONE')""")

###############################################################################################################
# Partner Table
###############################################################################################################

mycur.execute("""create table if not exists partner(Partner_Id integer PRIMARY KEY AUTOINCREMENT, 
	Name text NOT NULL DEFAULT 'NONE',
	Discord_Username text NOT NULL DEFAULT 'NONE',
	Address text NOT NULL DEFAULT 'NONE',
	Mail text NOT NULL DEFAULT 'NONE',
	Phone text NOT NULL DEFAULT 'NONE',
	Gender text NOT NULL DEFAULT 'NONE',
	Joined_At text NOT NULL DEFAULT 'NONE',
	Reference text NOT NULL DEFAULT 'NONE',
	Is_Active text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Community Table
###############################################################################################################

mycur.execute("""create table if not exists community(Id integer PRIMARY KEY AUTOINCREMENT,
	Name text NOT NULL DEFAULT 'NONE',
	Discord_Username text NOT NULL DEFAULT 'NONE',
	Mail text NOT NULL DEFAULT 'NONE',
	Phone text NOT NULL DEFAULT 'NONE',
	Gender text NOT NULL DEFAULT 'NONE',
	Joined_At text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Project Table
###############################################################################################################

mycur.execute("""create table if not exists project(Id integer PRIMARY KEY AUTOINCREMENT, 
	Name text NOT NULL DEFAULT 'NONE',
	Description text NOT NULL DEFAULT 'NONE',
	Hand_In_Date text NOT NULL DEFAULT 'NONE',
	Deadline text NOT NULL DEFAULT 'NONE',
	Hand_Out_Date text NOT NULL DEFAULT 'NONE',
	Client_Id text NOT NULL DEFAULT 'NONE',
	Amount_Id text NOT NULL DEFAULT 'NONE',
	Type text NOT NULL DEFAULT 'NONE',
	Status text NOT NULL DEFAULT 'NONE',
	Priority text NOT NULL DEFAULT 'NONE',
	Estimated_Amount text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Task Table
###############################################################################################################

mycur.execute("""create table if not exists task(Id integer PRIMARY KEY AUTOINCREMENT, 
	Title text NOT NULL DEFAULT 'NONE',
	Description text NOT NULL DEFAULT 'NONE',
	Assigned_To text NOT NULL DEFAULT 'NONE',
	Assigned_By text NOT NULL DEFAULT 'NONE',
	Status text NOT NULL DEFAULT 'NONE',
	Estimated_Time text NOT NULL DEFAULT 'NONE',
	Time_Taken text NOT NULL DEFAULT 'NONE',
	Estimated_XP integer NOT NULL DEFAULT 0,
	Given_XP integer NOT NULL DEFAULT 0,
	Project_Id text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Internal Table
###############################################################################################################

mycur.execute("""create table if not exists internal(Internal_Id integer PRIMARY KEY AUTOINCREMENT,
	Name text NOT NULL DEFAULT 'NONE',
	Address text NOT NULL DEFAULT 'NONE',
	DOB text NOT NULL DEFAULT 'NONE',
	Gender text NOT NULL DEFAULT 'NONE',
	Joined_At text NOT NULL DEFAULT 'NONE',
	Mail text NOT NULL DEFAULT 'NONE',
	Discord_Username text NOT NULL DEFAULT 'NONE',
	Phone text NOT NULL DEFAULT 'NONE',
	Whatsapp text NOT NULL DEFAULT 'NONE',
	Type text NOT NULL DEFAULT 'NONE',
	Is_Active text NOT NULL DEFAULT 'NONE',
	Total_XP integer NOT NULL DEFAULT 0,
	Level integer NOT NULL DEFAULT 0,
	Notes text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Suggestion Table
###############################################################################################################

mycur.execute("""create table if not exists suggestion(author text NOT NULL DEFAULT 'NONE', 
	number integer PRIMARY KEY AUTOINCREMENT, 
	title text NOT NULL DEFAULT 'NONE', 
	description text NOT NULL DEFAULT 'NONE', 
	reason text NOT NULL DEFAULT 'NONE', 
	is_considered integer NOT NULL DEFAULT 0, 
	considered_by text NOT NULL DEFAULT 'NONE'
	)""")

###############################################################################################################
# Career At Koders
###############################################################################################################
mycur.execute("""create table if not exists career_at_koders(Id integer PRIMARY KEY AUTOINCREMENT,
  Name text NOT NULL DEFAULT 'NONE',
  Address text NOT NULL DEFAULT 'NONE',
  Gender text NOT NULL DEFAULT 'NONE',
  DOB text NOT NULL DEFAULT 'NONE',
  Joined_At text NOT NULL DEFAULT 'NONE',
  Mail text NOT NULL DEFAULT 'NONE',
  Phone text NOT NULL DEFAULT 'NONE',
  Whatsapp text NOT NULL DEFAULT 'NONE'
  )""")


mydb.commit()


def insert(insert_query, value):
	mycur.execute(insert_query, value)
	mydb.commit()


def update(update_query, value):
	mycur.execute(update_query, value)
	mydb.commit()


def delete(delete_query, value):
	mycur.execute(delete_query, value)
	mydb.commit()


###############################################################################################################
# ON READY
###############################################################################################################

@client.event
async def on_ready():
	print("Integrity is ready and running on version {0}".format(info.version))


###############################################################################################################
# CHANNEL CREATION
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def create_channel(ctx, *, name):
	guild = ctx.guild
	member = ctx.message.author
	embed = discord.Embed(
		title = 'Want to create ticket for registering for **{}**'.format(name),
		description = 'React below with tick.',
		colour = discord.Colour.blue()
	)
	channel = await ctx.guild.create_text_channel(name=name, category=client.get_channel(setting.CHANNEL_ID))
	await channel.send(embed=embed)

###############################################################################################################
# ADDING REACTIONS TO MESSAGES
###############################################################################################################

@client.event
async def on_raw_reaction_add(payload):
	global count
	global channel_name
	# inputs = []
	
	message_id = payload.message_id
	channel_id = payload.channel_id
	guild_id = payload.guild_id
	user_id = payload.user_id
	member = payload.member

	try:
		def check(reaction, user):
			return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


		async def take_reaction():
			try:
				result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
			except asyncio.TimeoutError:
				await channel.send("Timeout. Please request a koder for reregistration.")
			else:
				reaction, user = result
				if (str(reaction.emoji) == '☑'):
					return True
				if (str(reaction.emoji) == '❎'):
					return False


		###############################################################################################################
		# for partner-with-us channel 
		###############################################################################################################

		if message_id == setting.PARTNER_EMBED_ID:
			count += 1
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			name=str(member.name) + '-' + str(count)
			embed = discord.Embed(
				title = '**{}** your ticket has been created for partner-with-us'.format(name),
				description = 'React below with **tick** to close your ticket',
				colour = discord.Colour.blue()
			)

			if payload.emoji.name == 'tick':
				channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))
				text = await channel.send(embed=embed)

				print(channel)

				await text.add_reaction(emoji="☑")

				ctx = channel

				await REGISTER.add_partner(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()

		###############################################################################################################
		# for career-at-koders channel 
		###############################################################################################################

		if message_id == setting.CAREER_AT_KODERS_EMBED_ID:
			count += 1
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			name=str(member.name) + '-' + str(count)

			embed = discord.Embed(
				title = '**{}** your ticket has been created for career-at-koders'.format(name),
				description = 'React below with **tick** to close your ticket',
				colour = discord.Colour.blue()
			)

			if payload.emoji.name == 'tick':
				channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))
				text = await channel.send(embed=embed)

				await text.add_reaction(emoji="☑")

				ctx = channel

				await REGISTER.add_career_at_koders(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()


		###############################################################################################################
		# for community-member channel 
		###############################################################################################################

		if message_id == setting.COMMUNITY_EMBED_ID:
			count += 1
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			name=str(member.name) + '-' + str(count)

			embed = discord.Embed(
				title = '**{}** your ticket has been created for community-member'.format(name),
				description = 'React below with **tick** to close your ticket',
				colour = discord.Colour.blue()
			)

			if payload.emoji.name == 'tick':
				channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))
				text = await channel.send(embed=embed)

				await text.add_reaction(emoji="☑")

				ctx = channel

				await REGISTER.add_community(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()


		###############################################################################################################
		# for project-registration channel 
		###############################################################################################################

		if message_id == setting.PROJECT_REGISTRATION_EMBED_ID:
			count += 1
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			name=str(member.name) + '-' + str(count)

			embed = discord.Embed(
				title = '**{}** your ticket has been created for project-registration'.format(name),
				description = 'React below with **tick** to close your ticket',
				colour = discord.Colour.blue()
			)

			if payload.emoji.name == 'tick':
				channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))
				text = await channel.send(embed=embed)

				await text.add_reaction(emoji="☑")

				ctx = channel

				await REGISTER.add_project(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()

		###############################################################################################################
		# for client-registration channel 
		###############################################################################################################

		if message_id == setting.CLIENT_REGISTRATION_EMBED_ID:
			count += 1
			
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			name=str(member.name) + '-' + str(count)

			embed = discord.Embed(
				title = '**{}** your ticket has been created for client-registration'.format(name),
				description = 'React below with **tick** to close your ticket',
				colour = discord.Colour.blue()
			)

			if payload.emoji.name == 'tick':
				channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))
				text = await channel.send(embed=embed)

				await text.add_reaction(emoji="☑")

				ctx = channel

				await REGISTER.add_client(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()


	except Exception as e:
		embed = discord.Embed(
			title="Exception Occured",
			description="{}".format(e)
		)
		async with aiohttp.ClientSession() as session:
			webhook = Webhook.from_url(setting.EXCEPTION_WEBHOOK, adapter=AsyncWebhookAdapter(session))
			await webhook.send(embed=embed)



###############################################################################################################
# REGISTER AS KODERS
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def internal(ctx):
	await REGISTER.add_member(client, ctx)


###############################################################################################################
# POLL COMMAND
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def poll(ctx, question, *options: str):
	embed = discord.Embed(
		title = question,
		colour = discord.Colour.blue()
	)
	if len(options) <= 1:
		await ctx.send('You need more than one option to make a poll!')
		return
	if len(options) > 4:
		await ctx.send('You cannot make a poll for more than 4 things!')
		return
	else:
		reactions = ['1⃣', '2⃣', '3⃣', '4⃣']

	description = []
	for x, option in enumerate(options):
	    description += '\n {} {}'.format(reactions[x], option)
	embed = discord.Embed(title=question, description=''.join(description))
	react_message = await ctx.send(embed=embed)
	for reaction in reactions[:len(options)]:
		await react_message.add_reaction(reaction)


###############################################################################################################
# MEME COMMAND
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def meme(ctx):
	try:
		response = requests.get('https://meme-api.herokuapp.com/gimme')
		response.raise_for_status()
		jsonResponse = response.json()
		url = jsonResponse["url"]
		await ctx.send(url)
	except Exception as error:
		print(error)
		await ctx.send(error)

###############################################################################################################
# MESSAGE LOGS
###############################################################################################################

@client.event
async def on_message_delete(message):
	if (not message.embeds):
		try:
			author = message.author.name
			content = message.content
			channel = message.channel

			embed = discord.Embed(
				title="Deleted Message",
				description="By {}".format(author),
				colour = discord.Colour.blue()
			)
			embed.add_field(name="Channel", value=channel, inline=False)
			embed.add_field(name="Message", value=content, inline=False)

			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url(setting.MESSAGE_WEBHOOK, adapter=AsyncWebhookAdapter(session))
				await webhook.send(embed=embed)
		except Exception as error:
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url(setting.EXCEPTION_WEBHOOK, adapter=AsyncWebhookAdapter(session))
				await webhook.send(error)


###############################################################################################################
# EXCEPTION LOGS
###############################################################################################################

@client.event
async def on_command_error(ctx, error):
	async with aiohttp.ClientSession() as session:
		webhook = Webhook.from_url(setting.EXCEPTION_WEBHOOK, adapter=AsyncWebhookAdapter(session))

		if isinstance(error, commands.CheckFailure):
			await webhook.send(error)
		elif isinstance(error, commands.CommandNotFound):
			await webhook.send(error)
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await webhook.send(error)
		elif isinstance(error, commands.TooManyArguments):
			await webhook.send(error)
		elif isinstance(error, commands.UserInputError):
			await webhook.send(error)
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await webhook.send(error)

		raise error


###############################################################################################################
# REGISTER TASK
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def task(ctx):
	await TASK.add_task(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def task_done(ctx, task_id: int):
	await TASK.task_done(client, ctx, task_id)


@client.command()
@commands.has_any_role('@everyone')
async def show_task(ctx, assigned_to, status):
	await TASK.show_task(client, ctx, assigned_to, status)


@client.command()
@commands.has_any_role('@everyone')
async def task_edit(ctx, task_id: int):
	await TASK.task_edit(client, ctx, task_id)


###############################################################################################################
# LEVEL SYSTEM
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def level(ctx, member: discord.Member):
	
	user_id = member.id
	user_id = f"<@!{user_id}>"
	
	user = str(member)
	try:
		mycur.execute("select Level from internal where Discord_Username = ?", (user_id, ))
		row = mycur.fetchone()
		level = row[0]
		await ctx.send("The level of {} is {}".format(member.mention, level))
	except Exception as error:
		await ctx.send("You are not registered as Koders.")


###############################################################################################################
# BIRTHDAY REMINDER
###############################################################################################################
async def birthday_reminder():

	channel = client.get_channel(setting.BIRTHDAY_ID)

	now = datetime.now()
	curmonth = now.month
	curday = now.day

	mycur.execute("select * from internal")
	rows = mycur.fetchall()
	for row in rows:
		internal_id = row[0]
		name = row[1]
		address = row[2]
		dob = row[3]
		gender = row[4]
		discord_username = row[7]


		dob = dob.split('/')
		day = dob[0]
		month = dob[1]

		if int(day) == int(curday):
			if int(month) == int(curmonth):
				await channel.send(f"Today is {discord_username} birthday.Happy birthday {discord_username} 🥳🥳🍕🍕")

	await asyncio.sleep(86400)


async def automatic_message():
	channel = client.get_channel(setting.GENERAL_CHANNEL)
	embed = discord.Embed(
		title = "opening and closing time is 11:00 AM and 8:00 PM"
	)
	embed.set_footer(text="Made by Koders Dev❤")
	now = datetime.now()
	day = date.today().weekday()
	current_time = now.strftime("%H:%M:%S")

	if day == 0 or day == 1 or day == 2 or day == 3 or day == 4 or day == 5:
		if current_time == "11:00:00":
			await channel.send(embed=embed)
			delay = 9*60*60
			await asyncio.sleep(delay)
		elif current_time == "20:00:00":
			await channel.send(embed=embed)
			delay = 15*60*60
			await asyncio.sleep(delay)

async def check_for_birthday():

	await client.wait_until_ready()
	while not client.is_closed():

		await birthday_reminder()
		await automatic_message()


###############################################################################################################
# 	SUGGESTION BOX
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def suggestion(ctx, title, description):
	await SUGGESTION_BOX.suggestion(client, ctx, title, description)

@client.command()
@commands.has_any_role('@everyone')
async def reply_suggestion(ctx, number: int, is_considered: int, reason):
	await SUGGESTION_BOX.reply_suggestion(client, ctx, number, is_considered, reason)

@client.command()
@commands.has_any_role('@everyone')
async def display(ctx, number: int):
	await SUGGESTION_BOX.display(client, ctx, number)


@client.command()
@commands.has_any_role('@everyone')
async def delete_suggestion(ctx, number: int):
	await SUGGESTION_BOX.delete_suggestion(client, ctx, number)

###############################################################################################################
# 	MUSIC PLAYLIST
###############################################################################################################

@client.command()
async def join(ctx):
	await MUSIC.join(client, ctx)


@client.command()
async def leave(ctx):
	await MUSIC.leave(client, ctx)


@client.command()
async def play(ctx, url: str):
	await MUSIC.play(client, ctx, url)


@client.command()
async def pause(ctx):
	await MUSIC.pause(client, ctx)


@client.command()
async def resume(ctx):
	await MUSIC.resume(client, ctx)


@client.command()
async def next(ctx):
	await MUSIC.next(client, ctx)


@client.command()
async def previous(ctx):
	await MUSIC.previous(client, ctx)


@client.command()
async def add(ctx, url: str):
	await MUSIC.add(client, ctx, url)


###############################################################################################################
# 	KICK BAN UNBAN
###############################################################################################################

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await KICK_BAN_UNBAN.kick(ctx, member, reason)


@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await KICK_BAN_UNBAN.ban(ctx, member, reason)


@client.command()
async def unban(ctx, *, member):
	await KICK_BAN_UNBAN.unban(ctx, member)

@client.command()
async def mute(ctx, member: discord.Member):
	await KICK_BAN_UNBAN.mute(ctx, member)


@client.command()
async def unmute(ctx, member: discord.Member):
	await KICK_BAN_UNBAN.unmute(ctx, member)

###############################################################################################################
# 	GAMES
###############################################################################################################

@client.command()
@commands.has_any_role('@everyone')
async def rps(ctx):
	await GAMES.rps(client, ctx)



@client.command()
@commands.has_any_role('@everyone')
async def er(ctx):
	await GAMES.er(client, ctx)



@client.command()
@commands.has_any_role('@everyone')
async def hm(ctx):
	await GAMES.hm(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def housie(ctx):
	await GAMES.housie(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def snake(ctx):
	await GAMES.snake(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def doc(ctx):
	await GAMES.doc(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def c4d(ctx):
	await GAMES.c4d(client, ctx)


@client.command()
@commands.has_any_role('@everyone')
async def bs(ctx):
	await GAMES.bs(client, ctx)


###############################################################################################################
# 	CYPHER INTEGRATION
###############################################################################################################
counter = {}

@client.event
async def on_message(message):
    file = open("bad.txt", "r")
    lines = file.readlines()
    for line in lines:
        line = line[:-1]
        if str(line) in message.content.lower().split(" "):
            author = message.author.name
            content = message.content
            from_channel = message.channel
            to_channel = client.get_channel(setting.BAD_WORD_CHANNEL)

            await message.delete()

            embed = discord.Embed(title="By {0}".format(author))
            embed.set_author(name="Used bad words")
            embed.add_field(name="Channel", value="{0}".format(from_channel), inline=False)
            embed.add_field(name="Message", value="{0}".format(content), inline=False)
            await to_channel.send(embed=embed)

            embed = discord.Embed(title="Reason", description="Bad words usage", color=0x2459bc)
            embed.set_author(name= message.author.name + " has been warned")
            await from_channel.send(embed=embed)

    if message.author in counter:
        counter[message.author] += 1
    else:
        counter[message.author] = 1

    author = message.author
    content = message.content
    channel = message.channel
    now = datetime.now()
    timestamp = str(datetime.timestamp(now))
    
    author_list = ['ninza_bot_test']
    
    with open('innovators.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, author.name, counter[author], content, channel])
    
    await client.process_commands(message)


###############################################################################################################
# 	PLOT USER ACTIVITY
###############################################################################################################

@client.command()
async def line_graph(ctx):
	await PLOT_USER_ACTIVITY.plot_user_activity(client, ctx)



# Global 		
@client.command()
async def ping(message):
    await message.send("Pong!")

@client.command()
@commands.has_any_role('@everyone')
async def logmywork(ctx):
    await work.worklog(client, ctx)

@client.command()
@commands.has_any_role('@everyone')
async def whoami(message):
    await message.send(message.author.name)


@client.command()
@commands.has_any_role('@everyone')
async def vision(ctx):
    await vs.vision(client, ctx)



# Koders
@client.command()
@commands.has_any_role('@everyone')
async def version(ctx):
	await ctx.send("Integrity is running on Version: {0}".format(info.version))

@client.command(pass_context=True)
@commands.has_any_role('@everyone')
async def clear(ctx, **args):
    channel = ctx.message.channel
    messages = []
    guild = ctx.message.guild
    async for entry in guild.audit_logs(limit=100):
        print('{0.user} did {0.action} to {0.target}'.format(entry))

@client.command(pass_context=True)
@commands.has_any_role('@everyone')
async def remind(ctx, *args):
    await ctx.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    author = ctx.author.name
    embed = discord.Embed(title="{0}".format(args[1]), color=0x2459bc)
    embed.set_author(name="Auto Reminder!")
    embed.set_thumbnail(url="http://image.flaticon.com/icons/svg/3079/3079046.svg")
    embed.add_field(name="Invoked by ", value="@{0}".format(author), inline=True)
    embed.add_field(name="Invoked for ", value="{0}".format(args[2]), inline=True)
    embed.set_footer(text="Made by Koders Dev")
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('@everyone')
async def overview(ctx):
    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel

    async def take_input():
        try:
            message = await client.wait_for('message', check=pred, timeout=44.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Try again later.")
        else:
            return message
    
    hours = ""
    textEmbed = await ctx.send("Enter all hours")
    textInput = await take_input()
    hours = textInput.content.split("\n")
    print(hours)
    await textInput.delete()
    await textEmbed.delete()

    users = ""
    textEmbed = await ctx.send("Enter all usernames")
    textInput = await take_input()
    users = textInput.content.split("\n")
    await textInput.delete()
    await textEmbed.delete()

    def unique(list1): 
        unique_list = [] 
        for x in list1: 
            if x not in unique_list: 
                unique_list.append(x) 
        return unique_list

    unique_users = unique(users)
    for i in range(0, len(unique_users)):
        x_axis = []
        y_axis = []
        total_hours = {}
        total_hours[unique_users[i]] = 0
        for j in range(0, len(users)):
            if(users[j] == unique_users[i]):
                x_axis.append(float(hours[j]))
                total_hours[unique_users[i]] += float(hours[j])
                y_axis.append(total_hours[unique_users[i]])
        x_axis.sort()
        plt.plot(x_axis, y_axis, marker='o', label=unique_users[i])
        plt.xlabel("Hours")
        plt.ylabel("Total hours")
        plt.title('Efficiency Management')
        plt.legend()
        plt.savefig('plot.png')
    plt.clf()
    await ctx.send("Overview", file=discord.File('plot.png', 'plot.png'))

client.loop.create_task(check_for_birthday())
client.run(TOKEN) 
mydb.close()