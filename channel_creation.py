import discord
from discord.ext import commands, tasks
import time
import asyncio
from datetime import datetime
import mysql.connector
import json
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

# MANUAL IMPORTS
import register_project as REGISTER_PROJECT
import register_member as REGISTER_MEMBER
import register_community as REGISTER_COMMUNITY
import settings as setting

TOKEN = setting.TOKEN
client = commands.Bot(command_prefix=".")

# mydb = mysql.connector.connect(host='localhost', user='root', password='', database='ticket')
# mycur = mydb.cursor(buffered=True)

count = 0


def insert(insert_query, value):
	mycur.execute(insert_query, value)
	mydb.commit()


@client.event
async def on_ready():
	print("Bot is ready.")

@client.command()
async def create_channel(ctx, *, name):
	guild = ctx.guild
	member = ctx.message.author
	# overwrite = discord.PermissionOverwrite()
	# overwrite.send_messages = False
	# overwrite.read_messages = True

	embed = discord.Embed(
		title = 'Want to create ticket for registering for **{}**'.format(name),
		description = 'React below with tick.',
		colour = discord.Colour.blue()
	)
	# ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
	channel = await ctx.guild.create_text_channel(name=name, category=client.get_channel(setting.CHANNEL_ID))
	await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
	global count
	global channel_name
	inputs = []
	
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


		# for partner-with-us channel #743395678948032532
		if message_id == 743395678948032532:
			count += 1
			# dict_counter['id'] += 1
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

				await REGISTER_MEMBER.add(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()


		# for career-at-koders channel #743395789061226516
		if message_id == 743395789061226516:
			count += 1
			# counter['id'] += 1
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
				# await text.add_reaction(emoji="❎")

				ctx = channel

				await REGISTER_MEMBER.add(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()

		# for community-member channel #743395901657317416
		if message_id == 743395901657317416:
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
				# await text.add_reaction(emoji="❎")

				ctx = channel

				await REGISTER_COMMUNITY.add(client, ctx, member)


				result = await take_reaction()

				if (result):
					await channel.delete()



		# for project-registration channel #743396000932036650
		if message_id == 743396000932036650:
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
				# await text.add_reaction(emoji="❎")

				ctx = channel

				await REGISTER_PROJECT.add(client, ctx, member)


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


@client.command()
async def register(ctx):
	await REGISTER_MEMBER.add(client, ctx)



@client.command()
async def project_registration(ctx):
	await REGISTER_PROJECT.add(client, ctx)


@client.command()
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



@client.command()
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


@client.event
async def on_message_delete(message):
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


@client.event
async def on_command_error(ctx, error):
	async with aiohttp.ClientSession() as session:
		webhook = Webhook.from_url(setting.EXCEPTION_WEBHOOK, adapter=AsyncWebhookAdapter(session))

		if isinstance(error, commands.CheckFailure):
			await webhook.send("You do not have the permission to do that.")
		elif isinstance(error, commands.CommandNotFound):
			await webhook.send(error)
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await webhook.send("Quote character is expected.")
		elif isinstance(error, commands.TooManyArguments):
			await webhook.send("Too many arguments used in invoking command. Check the number of arguments.")
		elif isinstance(error, commands.UserInputError):
			await webhook.send("Error occured while user enter some input")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await webhook.send("invalid end of wuoted string while invoking command.")

		raise error


client.run(TOKEN)