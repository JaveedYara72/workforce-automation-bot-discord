import discord
from discord.ext import commands
import time
import asyncio
import mysql.connector

TOKEN = "NzMzMjUzOTg4ODAzMjgwOTQ2.XxAd_g.vaNDVuOaapejDzCOyDnb0bws0Zs"
client = commands.Bot(command_prefix=".")

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='ticket')
mycur = mydb.cursor(buffered=True)

dict_counter = {'id':0}
dict_counter_c_at_koders = {'id':0}

count = 0

mycur.execute("select * from partner_with_us")
for row in mycur:
	dict_counter['id'] += 1

mycur.execute("select * from career_at_koders")
for row in mycur:
	dict_counter_c_at_koders['id'] += 1


def insert(insert_query, value):
	mycur.execute(insert_query, value)
	mydb.commit()


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
	channel = await ctx.guild.create_text_channel(name=name, category=client.get_channel(742716000650264607))
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
	if message_id == 742718907747532870:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))

	# for career-at-koders channel #742719341937557575
	if message_id == 742719341937557575:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))

	# for community-member channel #742719397264883732
	if message_id == 742719397264883732:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))


	# for project-registration channel #742719618879324282
	if message_id == 742719618879324282:
		count += 1
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id==guild_id, client.guilds)
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		name=str(member.name) + '-' + str(count)

		if payload.emoji.name == 'tick':
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))


@client.command()
async def register(ctx):
	inputs = []
	# dict_counter['id'] += 1 
	def pred(m):
		return m.author == ctx.author and m.channel == ctx.channel


	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=44.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=44.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	# Embed for name
	embed = discord.Embed(title="Hello there! (0/6)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for address
	embed = discord.Embed(title="Great, next step! (1/6)",
    	description="Please enter your address\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMotahaldu, haldwani, uttarakhand")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for gender
	embed = discord.Embed(title="Great, next step! (2/6)",
    	description="Please enter your gender\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMale/Female")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for DOB
	embed = discord.Embed(title="Great, next step! (3/6)",
    	description="Please enter your DOB\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n12-2-1999")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for whatsapp
	embed = discord.Embed(title="Great, next step! (4/6)",
    	description="Please enter your whatsapp\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n62XXXXXXXX")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for email
	embed = discord.Embed(title="Great, next step! (5/6)",
    	description="Please enter your email\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

    # Embed for phone
	embed = discord.Embed(title="Nice, next step! (6/6)",
                          description="Please enter your phone number\n(we won't spam, pinky promise again!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n9876543209")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	await ctx.send("enter anything to take current_timestamp")
	message = await take_input()
	timestamp = message.created_at

	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity", icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=False)
	embed.add_field(name="Address", value=inputs[1], inline=False)
	embed.add_field(name="Gender", value=inputs[2], inline=True)
	embed.add_field(name="DOB", value=inputs[3], inline=False)
	embed.add_field(name="Whatsapp", value=inputs[4], inline=False)
	embed.add_field(name="Email", value=inputs[5], inline=False)
	embed.add_field(name="Phone", value=inputs[6], inline=False)
	# embed.add_field(name="Id", value=dict_counter['id'], inline=False)
	embed.add_field(name="Joined-at", value=timestamp, inline=False)

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	address = inputs[1]
	gender = inputs[2]
	dob = inputs[3]
	whatsapp = inputs[4]
	email = inputs[5]
	phone = inputs[6]

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild
	# channel = discord.utils.get(guild.text_channels, name="partner-with-us")

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		# partner-with-us channel
		if channel.id == 742718903133929523:
			dict_counter['id'] += 1
			await ctx.send("Registration Completed at partner-with-us channel")
			insert_query = "insert into partner_with_us(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(%s, %s, %s, %s, %s, %s, %s, %s)"
			value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
			insert(insert_query, value)
		# career-at-koders channel
		elif channel.id == 742719337617424405:
			dict_counter_c_at_koders['id'] += 1
			await ctx.send("Registration Completed at career-at-koders channel")
			insert_query = "insert into career_at_koders(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(%s, %s, %s, %s, %s, %s, %s, %s)"
			value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
			insert(insert_query, value)
		# project-registration
		# elif channel.id == 742719613955080213:
		# 	dict_counter_c_at_koders['id'] += 1
		# 	await ctx.send("Registration Completed at project-registration channel")
		# 	insert_query = "insert into project_registration(Name, Description, Head_In_Date, Deadline, Teach_Stack) values(%s, %s, %s, %s, %s)"
		# 	value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
		# 	insert(insert_query, value)
		else:
			await ctx.send("invalid channel to done registration with!")

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")


client.run(TOKEN)
mydb.close()