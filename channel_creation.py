import discord
from discord.ext import commands
import time
import asyncio
#import mysql.connector

#MANUAL IMPORTS
import settings as setting
import register_member as REGISTER_MEMBER
TOKEN = setting.TOKEN
client = commands.Bot(command_prefix=".")

#mydb = mysql.connector.connect(host=setting.HOST, user=setting.USER, password=setting.PASSWORD, database=setting.DATABASE)
#mycur = mydb.cursor(buffered=True)
#
#dict_counter = {'id':0}
#dict_counter_c_at_koders = {'id':0}
#
#count = 0
#
#mycur.execute("select * from partner_with_us")
#for row in mycur:
#	dict_counter['id'] += 1
#
#mycur.execute("select * from career_at_koders")
#for row in mycur:
#	dict_counter_c_at_koders['id'] += 1
#
#
#def insert(insert_query, value):
#	mycur.execute(insert_query, value)
#	mydb.commit()


@client.event
async def on_ready():
	print("Bot is ready.")

@client.command()
async def create_channel(ctx, *, name):
	guild = ctx.message.guild
	member = ctx.message.author
	overwrite = discord.PermissionOverwrite()
	overwrite.send_messages = False
	overwrite.read_messages = True

	embed = discord.Embed(
		title = 'Having problem regarding **{}**'.format(name),
		description = 'React below with .',
		colour = discord.Colour.blue()
	)
	# ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
	channel = await ctx.guild.create_text_channel(name=name, category=client.get_channel(setting.CHANNEL_ID))
	await channel.set_permissions(member, overwrite=overwrite)
	await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
	global count
	global channel_name
	
	message_id = payload.message_id
	channel_id = payload.channel_id

	# def check(reaction, user):
	# 	return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


	# for partner-with-us channel #742718907747532870
	if message_id == setting.PARTNER_ID:
		count += 1
		guild_id = payload.guild_id guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))

	# for career-at-koders channel #742719341937557575
	if message_id == setting.CAREER_ID:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))

	# for community-member channel #742719397264883732
	if message_id == setting.COMMUNITY_ID:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))


	# for project-registration channel #742719618879324282
	if message_id == setting.PROJECT_ID:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(setting.TICKET_CHANNEL_ID))


@client.command()
async def register(ctx):
	await REGISTER_MEMBER.add(client, ctx)
client.run(TOKEN)
#mydb.close()
