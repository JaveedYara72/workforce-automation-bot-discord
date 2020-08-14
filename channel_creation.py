import discord
from discord.ext import commands
import time
import asyncio
import mysql.connector

TOKEN = "NzMzMjUzOTg4ODAzMjgwOTQ2.XxAd_g.vaNDVuOaapejDzCOyDnb0bws0Zs"
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
	channel = await ctx.guild.create_text_channel(name=name, category=client.get_channel(742716000650264607))
	await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
	global count
	global channel_name
	
	message_id = payload.message_id
	channel_id = payload.channel_id
	member = payload.member


	# for partner-with-us channel #743395678948032532
	if message_id == 743395678948032532:
		count += 1
		dict_counter['id'] += 1
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
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))
			text = await channel.send(embed=embed)


	# for career-at-koders channel #743395789061226516
	if message_id == 743395789061226516:
		count += 1
		counter['id'] += 1
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
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))
			await channel.send(embed=embed)

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
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))
			await channel.send(embed=embed)




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
			channel = await guild.create_text_channel(name=name, category=client.get_channel(742722032382509167))
			await channel.send(embed=embed)


@client.command()
async def register(ctx):
	inputs = []
	
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
	message = textInput

	timestamp = textInput.created_at
	
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

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
		if channel.id == 743395673545769021:
			await ctx.send("Registration Completed at partner-with-us channel")
			# insert_query = "insert into partner_with_us(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(%s, %s, %s, %s, %s, %s, %s, %s)"
			# value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
			# insert(insert_query, value)

		# career-at-koders channel
		elif channel.id == 743395784460075071:
			await ctx.send("Registration Completed at career-at-koders channel")
			# insert_query = "insert into career_at_koders(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(%s, %s, %s, %s, %s, %s, %s, %s)"
			# value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
			# insert(insert_query, value)

		else:
			await ctx.send("invalid channel to done registration with!")

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")



@client.command()
async def project_registration(ctx):
	inputs = []
	
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
	embed = discord.Embed(title="Hello there! (0/3)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for description
	embed = discord.Embed(title="Great, next step! (1/3)",
    	description="Please enter project-description\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nThis project is basically on registering the users to the different channels.")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for estimated-amount
	embed = discord.Embed(title="Great, next step! (2/3)",
    	description="Please enter your estimated-amount\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nRs 20 lakh ")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for source-material-links
	embed = discord.Embed(title="Great, next step! (3/3)",
    	description="Please enter source-material-links\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="""Example\nhttps://discordpy.readthedocs.io/en/latest/ext/commands/commands.html\n
		https://discordpy.readthedocs.io/en/latest/migrating.html""")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity", icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=False)
	embed.add_field(name="Description", value=inputs[1], inline=False)
	embed.add_field(name="Estimated-Amount", value=inputs[2], inline=True)
	embed.add_field(name="Source-Material-Links", value=inputs[3], inline=False)

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	description = inputs[1]
	estimated_amount = inputs[2]
	source_material_links = inputs[3]


	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		# project-registration
		if channel.id == 743395996003991622:
			await ctx.send("Registration Completed for project-registration")



client.run(TOKEN)
mydb.close()