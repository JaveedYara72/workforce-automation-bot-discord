import discord
from discord.ext import commands, tasks
import time
import asyncio
from datetime import datetime
import mysql.connector

# MANUAL IMPORTS
import register_project as REGISTER_PROJECT
import register_member as REGISTER_MEMBER
import register_community as REGISTER_COMMUNITY
import settings as setting

TOKEN = setting.TOKEN
client = commands.Bot(command_prefix=".")

# mydb = mysql.connector.connect(host='localhost', user='root', password='', database='ticket')
# mycur = mydb.cursor(buffered=True)

# dict_counter = {'id':0}
# counter = {'id':0}

count = 0

# mycur.execute("select * from partner_with_us")
# for row in mycur:
# 	dict_counter['id'] += 1

# mycur.execute("select * from career_at_koders")
# for row in mycur:
# 	counter['id'] += 1


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
			# channel_name = discord.utils.get(guild.text_channels, name=channel)

			await text.add_reaction(emoji="☑")
			# await text.add_reaction(emoji="❎")

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


@client.command()
async def register(ctx):
	await REGISTER_MEMBER.add(client, ctx)



@client.command()
async def project_registration(ctx):
	await REGISTER_PROJECT.add(client, ctx)



client.run(TOKEN)