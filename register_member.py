import discord
import asyncio
import datetime
import re
import mysql.connector
import settings as setting

# mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)

async def add(client, ctx, member):

	mydb = mysql.connector.connect(host="localhost", user="root", password="", database="ticket")
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
		# print(re.search(regex, email))

		if re.search(regex, email):
			return True
		else:
			return False


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
	# await gender_input.delete()
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

	if gender == '♂️':
		gender = "Male"
	elif gender == '♀':
		gender = "Female"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild
	# channel = discord.utils.get(guild.text_channels, name="partner-with-us")

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into partner_with_us(Name, Address, Gender, DOB, Joined_At, Mail, Phone, Whatsapp) values(%s, %s, %s, %s, %s, %s, %s, %s)"
		value = (name, address, gender, dob, timestamp, email, phone, whatsapp)
		insert(insert_query, value)
		await ctx.send("Registration Completed.")
		mydb.close()

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		mydb.close()