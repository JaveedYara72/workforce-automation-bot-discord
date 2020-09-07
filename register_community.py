import discord
import settings as setting
import re
import mysql.connector
import asyncio

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################

import html_email_template as HTML_TEMPLATE
import dm_template as DM_TEMPLATE


async def add(client, ctx, member):

	# For Database connectivity
	mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)
	mycur = mydb.cursor(buffered=True)
	inputs = []

	def insert(insert_query, value):
		mycur.execute(insert_query, value)
		mydb.commit()
	
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


	def validate_name(name):
		for letter in name:
			if letter in "0123456789" or len(name) < 3 or len(name.split()) > 3:
				return False
		return True

	
	def validate_phone(phone):
		for num in phone:
			if num not in "0123456789" or len(phone) != 10:
				return False
		return True
	
	
	def validate_email(email):
		regex = "^^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"
		# print(re.search(regex, email))

		if re.search(regex, email):
			return True
		else:
			return False


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
	embed.add_field(name="Name", value=inputs[0], inline=False)
	embed.add_field(name="Gender", value=inputs[1], inline=False)
	embed.add_field(name="Phone", value=inputs[2], inline=True)
	embed.add_field(name="Mail", value=inputs[3], inline=False)

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

		insert_query = "insert into community(Name, Discord_Username, Mail, Phone, Gender, Joined_At) values(%s, %s, %s, %s, %s, %s)"
		value = (name, discord_username, mail, phone, gender, timestamp)
		insert(insert_query, value)
		await ctx.send("Registration Completed for community.")
		
		await DM_TEMPLATE.dm_community(author)
		await HTML_TEMPLATE.Email_Community(mail, name)
		mydb.close()

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		mydb.close()