import discord
import asyncio
import datetime
import re
import settings as setting
import sqlite3


###############################################################################################################
# MANUAL IMPORT
###############################################################################################################
import leveling_system as LEVEL_SYSTEM
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


def update(update_query, value):
	mycur.execute(update_query, value)
	mydb.commit()


###############################################################################################################
# VALIDATION FUNCTION
###############################################################################################################
def validate_hour(hour):
	for number in hour:
		if number not in "0123456789":
			return False
	return True


###############################################################################################################
# GIVE TASK
###############################################################################################################
async def add_task(client, ctx):
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



	# Embed for Title
	embed = discord.Embed(title="Hello there! (0/5)",
    				description="Let's begin your registration with task.\n\nPlease enter title of your task.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMessage_Logs command")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	# Embed for Description
	embed = discord.Embed(title="Great, next step! (1/5)",
    	description="Please enter description of task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nThis is basically about creating a message_log command in discord")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	# Embed for Assigned_To
	embed = discord.Embed(title="Great, next step! (2/5)",
    	description="Please enter the name to whom the task is Assigned_To\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJhone doe")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)

	print(textInput.content)

	await textInput.delete()
	await textEmbed.delete()
	

	# Embed for Estimated_XP
	embed = discord.Embed(title="Great, next step! (3/5)",
    	description="Please enter **Estimated_XP** for the task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n50 XP")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()
	
	

	# Embed for Estimated_Time
	embed = discord.Embed(title="Great, next step! (4/5)",
    	description="Please enter Estimated_Time\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nNumbers of hours\n 6 or 8")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_hour(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_hour(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid hours. Re-enter no of hours")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	
	

    # Embed for Project_Id
	embed = discord.Embed(title="Nice, next step! (5/5)",
                          description="Please enter Project_Id\n(we won't spam, pinky promise again!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n12")
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


	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()
	
	


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Title", value=inputs[0], inline=True)
	embed.add_field(name="Description", value=inputs[1], inline=True)
	embed.add_field(name="Assigned_To", value=inputs[2], inline=True)
	embed.add_field(name="Estimated_XP", value=inputs[3], inline=True)
	embed.add_field(name="Estimated_Hours", value=inputs[4], inline=True)
	embed.add_field(name="Project_Id", value=inputs[5], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	title = inputs[0]
	description = inputs[1]
	assigned_to = inputs[2]
	estimated_xp = inputs[3]
	estimated_time = inputs[4]
	project_id = inputs[5]


	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "insert into task(Title, Description, Assigned_To, Estimated_XP, Estimated_Time, Project_Id, Assigned_By, Status) values(?, ?, ?, ?, ?, ?, ?, ?)"
		value = (title, description, assigned_to, estimated_xp, estimated_time, project_id, discord_username, "In_Progress")
		insert(insert_query, value)


		mycur.execute("select * from task order by Id desc limit 1;")
		row = mycur.fetchone()
		task_id = row[0]

		embed = discord.Embed(title="Task Details", description="Here are the details of the task.",
                          color=0x0e71c7)
		embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
		embed.add_field(name="Task_Id", value=task_id, inline=True)
		embed.add_field(name="Title", value=inputs[0], inline=True)
		embed.add_field(name="Description", value=inputs[1], inline=True)
		embed.add_field(name="Assigned_To", value=inputs[2], inline=True)
		embed.add_field(name="Estimated_XP", value=inputs[3], inline=True)
		embed.add_field(name="Estimated_Hours", value=inputs[4], inline=True)
		embed.add_field(name="Project_Id", value=inputs[5], inline=True)
		embed.add_field(name="Joined-at", value=timestamp, inline=True)
		embed.set_footer(text="Made by Koders Dev")


		task_updates_channel = client.get_channel(setting.TASK_UPDATES_CHANNEL_ID)

		await task_updates_channel.send(embed=embed)


		await ctx.send("Task Registration Completed.")

		time = int(estimated_time)

		#---------------------------------------

		await asyncio.sleep(time*60*60)

		await DEADLINE.add_deadline(ctx, task_id)

		#---------------------------------------

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")



async def show_task(client, ctx, assigned_to, status):
	
	mycur.execute("select * from task where Assigned_To = ? and Status = ?", (assigned_to, status))
	result = mycur.fetchall()

	for row in result:
		task_id = row[0]
		title = row[1]
		description = row[2]
		assigned_to = row[3]
		assigned_by = row[4]
		status = row[5]
		estimated_time = row[6]
		# time_taken = row[7]
		estimated_xp = row[8]
		# given_xp = row[9]
		project_id = row[10]


		embed = discord.Embed(title="Your Task", description="Details of the Task",
	                  color=0x0e71c7)
		embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
		embed.add_field(name="Task_id", value=task_id, inline=True)
		embed.add_field(name="Title", value=title, inline=True)
		embed.add_field(name="Description", value=description, inline=True)
		embed.add_field(name="Assigned_To", value=assigned_to, inline=True)
		embed.add_field(name="Assigned_By", value=assigned_by, inline=True)
		embed.add_field(name="Status", value=status, inline=True)
		embed.add_field(name="Estimated_Time", value=estimated_time, inline=True)
		embed.add_field(name="Estimated_XP", value=estimated_xp, inline=True)
		embed.add_field(name="Project_Id", value=project_id, inline=True)

		await ctx.send(embed=embed)



async def task_done(client, ctx, task_id):
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

	def status(reaction, user):
		return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author

	async def take_status():
		try:
			result = await client.wait_for('reaction_add', check=status, timeout=864.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			reaction, user = result
			if (str(reaction.emoji) == '☑'):
				return '☑'
			if (str(reaction.emoji) == '❎'):
				return '❎'



	# Embed for Time_Taken
	embed = discord.Embed(title="Great, next step! (0/2)",
    	description="Please enter Time_Taken to complete the task.\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n5hrs")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()
	
	if validate_hour(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_hour(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid hours. Re-enter no of hours")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()


	# Embed for Given_XP
	embed = discord.Embed(title="Great, next step! (1/2)",
    	description="Please enter **Given_XP** for the task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n50 XP")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()

	message = textInput
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	# Embed for Status
	embed = discord.Embed(title="Great, next step! (2/2)",
    	description="Please enter Status of the task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nreact with '☑' for Accepted\nreact with '❎' for Rejected")
	textEmbed = await ctx.send(embed=embed)
	
	await textEmbed.add_reaction(emoji="☑")
	await textEmbed.add_reaction(emoji="❎")

	react = await take_status()

	inputs.append(react)
	await textEmbed.delete()


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Time_Taken", value=inputs[0], inline=True)
	embed.add_field(name="Given_XP", value=inputs[1], inline=True)
	embed.add_field(name="Status", value=inputs[2], inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)
	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	time_taken = inputs[0]
	given_xp = inputs[1]
	status = inputs[2]

	if status == '☑':
		status = "Accepted"
	elif status == '❎':
		status = "Rejected"

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		insert_query = "update task set Time_Taken = ?, Given_XP = ?, Status = ? where Id = ?"
		value = (time_taken, given_xp, status, task_id)
		insert(insert_query, value)

		mycur.execute("select * from task where id = ?", (task_id, ))
		row = mycur.fetchone()
		title = row[1]
		description = row[2]
		assigned_to = row[3]
		assigned_by = row[4]
		status = row[5]
		estimated_time = row[6]
		time_taken = row[7]
		estimated_xp = row[8]
		given_xp = row[9]
		project_id = row[10]

		if status == "Accepted":
			embed = discord.Embed(title="Accepted Task", description="Details of the Task",
                          color=0x0e71c7)
			embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
			embed.add_field(name="Task_id", value=task_id, inline=True)
			embed.add_field(name="Title", value=title, inline=True)
			embed.add_field(name="Description", value=description, inline=True)
			embed.add_field(name="Assigned_To", value=assigned_to, inline=True)
			embed.add_field(name="Assigned_By", value=assigned_by, inline=True)
			embed.add_field(name="Status", value=status, inline=True)
			embed.add_field(name="Estimated_Time", value=estimated_time, inline=True)
			embed.add_field(name="Time_Taken", value=time_taken, inline=True)
			embed.add_field(name="Estimated_XP", value=estimated_xp, inline=True)
			embed.add_field(name="Given_XP", value=given_xp, inline=True)
			embed.add_field(name="Project_Id", value=project_id, inline=True)
			embed.set_footer(text="Made by Koders Dev")

			accepted_task_channel = client.get_channel(setting.ACCEPTED_TASK_CHANNEL_ID)

			await accepted_task_channel.send(embed=embed)

		await LEVEL_SYSTEM.add(ctx, assigned_to)



async def task_edit(client, ctx, task_id):
	inputs = []

	mycur.execute("select * from task where Id = ?", (task_id, ))
	row = mycur.fetchone()
	title = row[1]
	description = row[2]
	assigned_to = row[3]
	status = row[5]
	estimated_time = row[6]
	estimated_xp = row[8]

	embed = discord.Embed(title="Task Details", description="The details of task with id #{} is:".format(task_id))
	embed.add_field(name="Id", value=task_id, inline=True)
	embed.add_field(name="Title", value=title, inline=True)
	embed.add_field(name="Description", value=description, inline=True)
	embed.add_field(name="Assigned_To", value=assigned_to, inline=True)
	embed.add_field(name="Status", value=status, inline=True)
	embed.add_field(name="Estimated_Time", value=estimated_time, inline=True)
	embed.add_field(name="Estimated_XP", value=estimated_xp, inline=True)

	text = await ctx.send(embed=embed)

	
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


	# Embed for Title
	embed = discord.Embed(title="Hello there! (0/5)",
    				description="Let's begin with editing task.\n\nPlease enter title of your task.")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nMessage_Logs command")
	textEmbed = await ctx.send(embed=embed)
	textInput = await take_input()

	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()


	# Embed for Description
	embed = discord.Embed(title="Great, next step! (1/5)",
    	description="Please enter description of task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nThis is basically about creating a message_log command in discord")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()

	# Embed for Assigned_To
	embed = discord.Embed(title="Great, next step! (2/5)",
    	description="Please enter the name to whom the task is Assigned_To\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nJhone doe")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)

	print(textInput.content)

	await textInput.delete()
	await textEmbed.delete()
	

	# Embed for Estimated_XP
	embed = discord.Embed(title="Great, next step! (3/5)",
    	description="Please enter **Estimated_XP** for the task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\n50 XP")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()
	
	

	# Embed for Estimated_Time
	embed = discord.Embed(title="Great, next step! (4/5)",
    	description="Please enter Estimated_Time\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nNumbers of hours\n 6 or 8")
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

	if validate_hour(textInput.content):
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()
	else:
		while validate_hour(textInput.content) != True:
			await textInput.delete()
			await textEmbed.delete()
			text = await ctx.send("Invalid hours. Re-enter no of hours")
			textEmbed = await ctx.send(embed=embed)
			textInput = await take_input()
			await text.delete()
		inputs.append(textInput.content)
		await textInput.delete()
		await textEmbed.delete()


	# Embed for Status
	embed = discord.Embed(title="Great, next step! (5/5)",
    	description="Please enter status of task\n(we won't spam, pinky promise!)")
	embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
	embed.set_footer(text="Example\nIn_Progress, Completed")
	textEmbed = await ctx.send(embed=embed)

	textInput = await take_input()
	inputs.append(textInput.content)
	await textInput.delete()
	await textEmbed.delete()
	


	embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
	embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity")
	embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
	embed.add_field(name="Id", value=task_id, inline=True)
	embed.add_field(name="Title", value=inputs[0], inline=True)
	embed.add_field(name="Description", value=inputs[1], inline=True)
	embed.add_field(name="Assigned_To", value=inputs[2], inline=True)
	embed.add_field(name="Estimated_XP", value=inputs[3], inline=True)
	embed.add_field(name="Estimated_Hours", value=inputs[4], inline=True)
	embed.add_field(name="Status", value=inputs[5], inline=True)
	embed.add_field(name="Joined-at", value=timestamp, inline=True)
	embed.set_footer(text="Made by Koders Dev")

	text = await ctx.send(embed=embed)


	await text.add_reaction(emoji="☑")
	await text.add_reaction(emoji="❎")

	title = inputs[0]
	description = inputs[1]
	assigned_to = inputs[2]
	estimated_xp = inputs[3]
	estimated_time = inputs[4]
	status = inputs[5]

	result = await take_reaction()
	await text.delete()

	guild = ctx.guild

	channel = discord.utils.find(lambda c : c.id==message.channel.id, guild.channels)

	if (result):
		update_query = "update task set Title = ?, Description = ?, Assigned_To = ?, Estimated_XP = ?, Estimated_Time = ?, Status = ? where Id = ?"
		value = (title, description, assigned_to, estimated_xp, estimated_time, status, task_id)
		update(update_query, value)

		await ctx.send("The task with id {} has been edited succesfully.".format(task_id))

		task_edit_channel = client.get_channel(setting.TASK_EDIT_CHANNEL_ID)

		mycur.execute("select * from task where Id = ?", (task_id, ))
		row = mycur.fetchone()
		title = row[1]
		description = row[2]
		assigned_to = row[3]
		status = row[5]
		estimated_time = row[6]
		estimated_xp = row[8]

		embed = discord.Embed(title="Task Details", description="The details of task with id #{} is:".format(task_id))
		embed.add_field(name="Id", value=task_id, inline=True)
		embed.add_field(name="Title", value=title, inline=True)
		embed.add_field(name="Description", value=description, inline=True)
		embed.add_field(name="Assigned_To", value=assigned_to, inline=True)
		embed.add_field(name="Status", value=status, inline=True)
		embed.add_field(name="Estimated_Time", value=estimated_time, inline=True)
		embed.add_field(name="Estimated_XP", value=estimated_xp, inline=True)
		embed.set_footer(text="Made by Koders Dev")

		text = await task_edit_channel.send(embed=embed)

