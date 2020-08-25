import discord
import settings as setting
import mysql.connector
from datetime import date

async def add(client, ctx, member):

	# For Database
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

	def validate_name(name):
		for letter in name:
			if letter in "0123456789" or len(name) < 3 or len(name.split()) > 3:
				return False
		return True


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
	embed.add_field(name="Name", value=inputs[0], inline=False)
	embed.add_field(name="Description", value=inputs[1], inline=False)
	embed.add_field(name="Estimated-Amount", value=inputs[2], inline=True)
	embed.add_field(name="Deadline", value=inputs[3], inline=False)

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	name = inputs[0]
	description = inputs[1]
	estimated_amount = inputs[2]
	deadline = inputs[3]

	hand_in_date = date.today()


	# This part needs to be handled by try except clause
	mycur.execute("select Id from client where Name = %s", (name, ))
	row = mycur.fetchone()
	client_id = row[0]


	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into project(Name, Description, Hand_In_Date, Deadline, Client_Id, Status, Priority, Estimated_Amount) values(%s, %s, %s, %s, %s, %s, %s, %s)"
		value = (name, description, hand_in_date, deadline, client_id, "On Hold", "High", estimated_amount)
		insert(insert_query, value)
		await ctx.send("Registration Completed for project-registration")
		mydb.close()

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		mydb.close()