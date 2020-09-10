import discord
import asyncio
import datetime
import re
import aiohttp
import settings as setting
import sqlite3
from discord import Webhook, AsyncWebhookAdapter

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################

# import email_template as EMAIL_TEMPLATE
import html_email_template as HTML_TEMPLATE
import leveling_system as LEVEL_SYSTEM
import dm_template as DM_TEMPLATE
import deadline_cross_reminder as DEADLINE

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
# DATABASE QUERIES
###############################################################################################################
def insert(insert_query, value):
	mycur.execute(insert_query, value)
	mydb.commit()



###############################################################################################################
# VALIDATION FUNCTIONS
###############################################################################################################
def validate_name(name):
	for letter in name:
		if letter in "0123456789" or len(name) < 3 or len(name.split()) > 3:
			return False
	return True

	
def validate_dob(dob):
	try:
		dob = datetime.datetime.strptime(dob,'%d/%m/%Y')
		return True
	except ValueError:
		return False


def validate_phone(phone):
	for num in phone:
		if num not in "0123456789" or len(phone) != 10:
			return False
	return True


def validate_email(email):
	regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"

	if re.search(regex, email):
		return True
	else:
		return False



###############################################################################################################
# ADD MEMBER
###############################################################################################################

async def add_member(client, ctx):
	inputs = []

	def pred(m):
		return m.author == ctx.author and m.channel == ctx.channel


	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	def gender(reaction, user):
		return (str(reaction.emoji) == '♂️' or str(reaction.emoji) == '♀') and user == ctx.message.author


	async def take_gender():
		try:
			result = await client.wait_for('reaction_add', check=gender, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '♂️'):
				return '♂️'
			if (str(reaction.emoji) == '♀'):
				return '♀'


	# Embed for name
	embed = discord.Embed(title="Hello there! (0/7)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_name(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_name(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()



	# Embed for address
	embed = discord.Embed(title="Great, next step! (1/7)",
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
	embed = discord.Embed(title="Great, next step! (2/7)",
    	description="Please enter your gender\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMale/Female")
	textEmbed = await ctx.send(embed=embed)
	
	await textEmbed.add_reaction(emoji="♂️")
	await textEmbed.add_reaction(emoji="♀")

	gender_input = await take_gender()
	inputs.append(gender_input)
	await textEmbed.delete()


	# Embed for DOB
	embed = discord.Embed(title="Great, next step! (3/7)",
    	description="Please enter your DOB\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n12/2/1999")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_dob(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_dob(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid DOB. Re-enter your DOB")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for whatsapp
	embed = discord.Embed(title="Great, next step! (4/7)",
    	description="Please enter your whatsapp\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n62XXXXXXXX")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid whatsapp. Re-enter your whatsapp no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for email
	embed = discord.Embed(title="Great, next step! (5/7)",
    	description="Please enter your email\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_email(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_email(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid email. Re-enter your email")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

    # Embed for phone
	embed = discord.Embed(title="Nice, next step! (6/7)",
                          description="Please enter your phone number\n(we won't spam, pinky promise again!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n9876543209")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput

	timestamp = textInput.created_at
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]
	
	discord_username = textInput.author
	author = textInput.author

	user_id = author.id
	
	discord_username = str(discord_username)

	username, client_id = discord_username.split('#')
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid phone no. Re-enter your phone no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()


	# Embed for notes
	embed = discord.Embed(title="Great, next step! (7/7)",
    	description="Please enter your notes\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	inputs.append(textInput.content)

	await textInput.delete()
	await textEmbed.delete()

	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Address", value=inputs[1], inline=True)
	embed.add_field(name="Gender", value=inputs[2], inline=True)
	embed.add_field(name="DOB", value=inputs[3], inline=True)
	embed.add_field(name="Whatsapp", value=inputs[4], inline=True)
	embed.add_field(name="Email", value=inputs[5], inline=True)
	embed.add_field(name="Phone", value=inputs[6], inline=True)
	embed.add_field(name="Notes", value=inputs[7], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

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
	notes = inputs[7]

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into internal(Name, Address, Gender, DOB, Discord_Username, Mail, Phone, Whatsapp, Notes, Joined_At, Is_Active) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		user_id = f"<@!{user_id}>"
		value = (name, address, gender, dob, user_id, email, phone, whatsapp, notes, timestamp, "True")
		insert(insert_query, value)
		await ctx.send("Registration Completed.")
		
		await DM_TEMPLATE.dm_koders(author)


	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
# ADD CLIENT
###############################################################################################################

async def add_client(client, ctx, member):
	inputs = []
	
	def pred(m):
		return m.author == member and m.channel == ctx


	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	def gender(reaction, user):
		return (str(reaction.emoji) == '♂️' or str(reaction.emoji) == '♀') and user == member

	async def take_gender():
		try:
			result = await client.wait_for('reaction_add', check=gender, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '♂️'):
				return '♂️'
			if (str(reaction.emoji) == '♀'):
				return '♀'



	# Embed for name
	embed = discord.Embed(title="Hello there! (0/6)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_name(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_name(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()



	# Embed for address
	embed = discord.Embed(title="Great, next step! (1/7)",
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
	embed = discord.Embed(title="Great, next step! (2/7)",
    	description="Please enter your gender\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMale/Female")
	textEmbed = await ctx.send(embed=embed)
	
	await textEmbed.add_reaction(emoji="♂️")
	await textEmbed.add_reaction(emoji="♀")

	gender_input = await take_gender()
	inputs.append(gender_input)
	await textEmbed.delete()


	# Embed for DOB
	embed = discord.Embed(title="Great, next step! (3/7)",
    	description="Please enter your DOB\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n12/2/1999")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_dob(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_dob(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid DOB. Re-enter your DOB")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for whatsapp
	embed = discord.Embed(title="Great, next step! (4/7)",
    	description="Please enter your whatsapp\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n62XXXXXXXX")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid whatsapp. Re-enter your whatsapp no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for email
	embed = discord.Embed(title="Great, next step! (5/7)",
    	description="Please enter your email\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_email(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_email(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid email. Re-enter your email")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

    # Embed for phone
	embed = discord.Embed(title="Nice, next step! (6/7)",
                          description="Please enter your phone number\n(we won't spam, pinky promise again!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n9876543209")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput

	timestamp = textInput.created_at
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]


	discord_username = textInput.author
	
	author = textInput.author
	discord_username = str(discord_username)

	username, client_id = discord_username.split('#')
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid phone no. Re-enter your phone no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()


	# Embed for notes
	embed = discord.Embed(title="Great, next step! (7/7)",
    	description="Please enter your notes\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	inputs.append(textInput.content)

	await textInput.delete()
	await textEmbed.delete()

	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Address", value=inputs[1], inline=True)
	embed.add_field(name="Gender", value=inputs[2], inline=True)
	embed.add_field(name="DOB", value=inputs[3], inline=True)
	embed.add_field(name="Whatsapp", value=inputs[4], inline=True)
	embed.add_field(name="Email", value=inputs[5], inline=True)
	embed.add_field(name="Phone", value=inputs[6], inline=True)
	embed.add_field(name="Notes", value=inputs[7], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

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
	notes = inputs[7]

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild
	
	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into client(Id, Name, Address, Gender, DOB, Discord_Username, Mail, Phone, Whatsapp, Notes) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		value = (client_id, name, address, gender, dob, discord_username, email, phone, whatsapp, notes)
		insert(insert_query, value)
		await ctx.send("Registration Completed.")
		
		await DM_TEMPLATE.dm_client(author)
		

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
# ADD COMMUNITY
###############################################################################################################

async def add_community(client, ctx, member):
	inputs = []
	
	def pred(m):
		return m.author == member and m.channel == ctx

	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False

	def gender(reaction, user):
		return (str(reaction.emoji) == '♂️' or str(reaction.emoji) == '♀') and user == member

	async def take_gender():
		try:
			result = await client.wait_for('reaction_add', check=gender, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '♂️'):
				return '♂️'
			if (str(reaction.emoji) == '♀'):
				return '♀'


	# Embed for name
	embed = discord.Embed(title="Hello there! (0/3)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_name(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_name(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for gender
	embed = discord.Embed(title="Great, next step! (1/3)",
    	description="Please enter your gender\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n")
	textEmbed = await ctx.send(embed=embed)
	
	await textEmbed.add_reaction(emoji="♂️")
	await textEmbed.add_reaction(emoji="♀")

	gender_input = await take_gender()

	inputs.append(gender_input)
	await textEmbed.delete()

	# Embed for phone
	embed = discord.Embed(title="Great, next step! (2/3)",
    	description="Please enter your phone no.\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n728746XXXX")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	timestamp = textInput.created_at
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]

	discord_username = textInput.author
	author = textInput.author
	discord_username = str(discord_username)

	username, client_id = discord_username.split('#')
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	# Embed for mail
	embed = discord.Embed(title="Great, next step! (3/3)",
    	description="Please enter mail\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="""Example\njane@gmail.com""")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput
	
	if validate_email(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_email(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Gender", value=inputs[1], inline=True)
	embed.add_field(name="Phone", value=inputs[2], inline=True)
	embed.add_field(name="Mail", value=inputs[3], inline=True)
	embed.add_field(name="Joined_At", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	gender = inputs[1]
	phone = inputs[2]
	mail = inputs[3]

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"


	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):

		insert_query = "insert into community(Name, Discord_Username, Mail, Phone, Gender, Joined_At) values(?, ?, ?, ?, ?, ?)"
		value = (name, discord_username, mail, phone, gender, timestamp)
		insert(insert_query, value)
		await ctx.send("Registration Completed for community.")
		
		await DM_TEMPLATE.dm_community(author)
		await HTML_TEMPLATE.Email_Community(mail, name)
		

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
# ADD CAREER AT KODERS
###############################################################################################################

async def add_career_at_koders(client, ctx, member):
	inputs = []
	
	def pred(m):
		return m.author == member and m.channel == ctx


	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	def gender(reaction, user):
		return (str(reaction.emoji) == '♂️' or str(reaction.emoji) == '♀') and user == member

	async def take_gender():
		try:
			result = await client.wait_for('reaction_add', check=gender, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '♂️'):
				return '♂️'
			if (str(reaction.emoji) == '♀'):
				return '♀'


	# Embed for name
	embed = discord.Embed(title="Hello there! (0/6)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_name(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_name(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
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
	
	await textEmbed.add_reaction(emoji="♂️")
	await textEmbed.add_reaction(emoji="♀")

	gender_input = await take_gender()

	inputs.append(gender_input)
	await textEmbed.delete()

	# Embed for DOB
	embed = discord.Embed(title="Great, next step! (3/6)",
    	description="Please enter your DOB\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n12/2/1999")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_dob(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_dob(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid DOB. Re-enter your DOB")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
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
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid whatsapp. Re-enter your whatsapp no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
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
	
	if validate_email(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_email(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid email. Re-enter your email")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
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
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]

	discord_username = textInput.author
	author = textInput.author
	discord_username = str(discord_username)

	username, client_id = discord_username.split('#')
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid phone no. Re-enter your phone no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Address", value=inputs[1], inline=True)
	embed.add_field(name="Gender", value=inputs[2], inline=True)
	embed.add_field(name="DOB", value=inputs[3], inline=True)
	embed.add_field(name="Whatsapp", value=inputs[4], inline=True)
	embed.add_field(name="Email", value=inputs[5], inline=True)
	embed.add_field(name="Phone", value=inputs[6], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

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

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into career_at_koders(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(?, ?, ?, ?, ?, ?, ?, ?)"
		value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
		insert(insert_query, value)
		await ctx.send("Registration Completed.")

		await DM_TEMPLATE.dm_career(author)
		await HTML_TEMPLATE.Email_Career_At_Koders(email, name)
		

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
# ADD PARTNER
###############################################################################################################

async def add_partner(client, ctx, member):
	inputs = []

	def pred(m):
		return m.author == member and m.channel == ctx


	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	def gender(reaction, user):
		return (str(reaction.emoji) == '♂️' or str(reaction.emoji) == '♀') and user == member

	async def take_gender():
		try:
			result = await client.wait_for('reaction_add', check=gender, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '♂️'):
				return '♂️'
			if (str(reaction.emoji) == '♀'):
				return '♀'


	# Embed for name
	embed = discord.Embed(title="Hello there! (0/5)",
    				description="Let's begin your registration.\n\nPlease enter your full name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJane Doe")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	if validate_name(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_name(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid Name. Re-enter your name")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()



	# Embed for address
	embed = discord.Embed(title="Great, next step! (1/5)",
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
	embed = discord.Embed(title="Great, next step! (2/5)",
    	description="Please enter your gender\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMale/Female")
	textEmbed = await ctx.send(embed=embed)
	
	await textEmbed.add_reaction(emoji="♂️")
	await textEmbed.add_reaction(emoji="♀")

	gender_input = await take_gender()

	inputs.append(gender_input)
	await textEmbed.delete()


	# Embed for Reference
	embed = discord.Embed(title="Great, next step! (3/5)",
    	description="Please enter Reference\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nName of person or company")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	inputs.append(textInput.content)

	await textInput.delete()
	await textEmbed.delete()


	# Embed for email
	embed = discord.Embed(title="Great, next step! (4/5)",
    	description="Please enter your email\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\njane@gmail.com")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_email(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_email(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid email. Re-enter your email")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

    # Embed for phone
	embed = discord.Embed(title="Nice, next step! (5/5)",
                          description="Please enter your phone number\n(we won't spam, pinky promise again!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n9876543209")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput

	timestamp = textInput.created_at
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]

	discord_username = textInput.author
	author = textInput.author
	discord_username = str(discord_username)

	username, client_id = discord_username.split('#')
	
	if validate_phone(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_phone(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid phone no. Re-enter your phone no.")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()

	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Address", value=inputs[1], inline=True)
	embed.add_field(name="Gender", value=inputs[2], inline=True)
	embed.add_field(name="Reference", value=inputs[3], inline=True)
	embed.add_field(name="Email", value=inputs[4], inline=True)
	embed.add_field(name="Phone", value=inputs[5], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	address = inputs[1]
	gender = inputs[2]
	reference = inputs[3]
	email = inputs[4]
	phone = inputs[5]

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into partner(Name, Discord_Username, Address, Mail, Phone, Gender, Joined_At, Reference, Is_Active) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
		value = (name, discord_username, address, email, phone, gender, timestamp, reference, "True")
		insert(insert_query, value)
		await ctx.send("Registration Completed.")
		await DM_TEMPLATE.dm_partner(author)
		

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
# ADD PROJECT
###############################################################################################################

async def add_project(client, ctx, member):
	inputs = []
	
	def pred(m):
		return m.author == member and m.channel == ctx

	def check(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == member


	async def take_input():
		try:
			message = await client.wait_for('message', check=pred, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return message


	async def take_reaction():
		try:
			result = await client.wait_for('reaction_add', check=check, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return True
			if (str(reaction.emoji) == '❎'):
				return False


	# Embed for project name
	embed = discord.Embed(title="Hello there! (0/3)",
    				description="Let's begin your registration.\n\nPlease enter your project name.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nDiscord bot")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for project description
	embed = discord.Embed(title="Great, next step! (1/3)",
    	description="Please enter project-description\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nThis project is basically on registering the users to the different channels.")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	timestamp = textInput.created_at
	timestamp = str(timestamp)
	timestamp = timestamp.split('.')
	timestamp = timestamp[0]

	discord_username = textInput.author
	author = textInput.author
	discord_username = str(discord_username)


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

	# Embed for Deadline
	embed = discord.Embed(title="Great, next step! (3/3)",
    	description="Please enter deadline\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="""Example\n7/1/2021""")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	message = textInput
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Name", value=inputs[0], inline=True)
	embed.add_field(name="Description", value=inputs[1], inline=True)
	embed.add_field(name="Estimated-Amount", value=inputs[2], inline=True)
	embed.add_field(name="Deadline", value=inputs[3], inline=True)
	embed.add_field(name="Joined_At", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	description = inputs[1]
	estimated_amount = inputs[2]
	deadline = inputs[3]

	hand_in_date = datetime.date.today()


	# This part needs to be handled by try except clause
	try:
		mycur.execute("select Id, Mail, Name from client where Discord_Username = ?", (discord_username, ))
		row = mycur.fetchone()

		if row:
			client_id = row[0]
			email = row[1]
			client_name = row[2]
		else:
			await ctx.send("you are not a client. First register as client.")

	except Exception as error:
		async with aiohttp.ClientSession() as session:
			webhook = Webhook.from_url(setting.EXCEPTION_WEBHOOK, adapter=AsyncWebhookAdapter(session))
			await webhook.send(error)


	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into project(Name, Description, Hand_In_Date, Deadline, Client_Id, Status, Priority, Estimated_Amount) values(?, ?, ?, ?, ?, ?, ?, ?)"
		value = (name, description, hand_in_date, deadline, client_id, "On Hold", "High", estimated_amount)
		insert(insert_query, value)
		await ctx.send("Registration Completed for project-registration")
		await DM_TEMPLATE.dm_project(author)
		
		await HTML_TEMPLATE.Email_Project_Registration(email, client_name)

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		



###############################################################################################################
