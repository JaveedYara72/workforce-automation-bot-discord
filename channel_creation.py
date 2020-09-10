import discord
from discord.ext import commands, tasks
import time
import asyncio
import datetime
from datetime import date
import json
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import sqlite3


###############################################################################################################
# MANUAL IMPORTS
###############################################################################################################
import register as REGISTER
import task as TASK
import suggestion_box as SUGGESTION_BOX
import settings as setting


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


# mycur.execute("drop table client")
# mycur.execute("drop table partner")
# mycur.execute("drop table community")
# mycur.execute("drop table project")
# mycur.execute("drop table task")
# mycur.execute("drop table internal")
# mycur.execute("drop table suggestion")
# mycur.execute("drop table employee")
# mycur.execute("drop table career_at_koders")
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
	print("Bot is ready.")


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

async def check_for_birthday():

	await client.wait_until_ready()
	now = datetime.datetime.now()
	curmonth = now.month
	curday = now.day

	while not client.is_closed():
		channel = client.get_channel(setting.BIRTHDAY_ID)

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



client.loop.create_task(check_for_birthday())
client.run(TOKEN) 
mydb.close()