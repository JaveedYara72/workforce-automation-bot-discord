import discord
import asyncio
import datetime
import re
import mysql.connector
import settings as setting

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################

import email_template as EMAIL_TEMPLATE
import leveling_system as LEVEL_SYSTEM
import deadline_cross_reminder as DEADLINE


async def add(client, ctx):

	mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)
	mycur = mydb.cursor(buffered=True)
	inputs = []

	def insert(insert_query, value):
		mycur.execute(insert_query, value)
		mydb.commit()


	def update(update_query, value):
		mycur.execute(update_query, value)
		mydb.commit()

	
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
	embed.add_field(name="Title", value=inputs[0], inline=False)
	embed.add_field(name="Description", value=inputs[1], inline=False)
	embed.add_field(name="Assigned_To", value=inputs[2], inline=False)
	embed.add_field(name="Estimated_XP", value=inputs[3], inline=True)
	embed.add_field(name="Estimated_Hours", value=inputs[4], inline=False)
	embed.add_field(name="Project_Id", value=inputs[5], inline=False)
	embed.add_field(name="Joined-at", value=timestamp, inline=False)

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
		insert_query = "insert into task(Title, Description, Assigned_To, Estimated_XP, Estimated_Time, Project_Id, Assigned_By, Status) values(%s, %s, %s, %s, %s, %s, %s, %s)"
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

		task_updates_channel = client.get_channel(setting.TASK_UPDATES_CHANNEL_ID)

		await task_updates_channel.send(embed=embed)


		await ctx.send("Task Registration Completed.")

		time = int(estimated_time)

		#---------------------------------------

		await asyncio.sleep(time*60*60)

		await DEADLINE.add(ctx, task_id)

		#---------------------------------------
		mydb.close()

	else:
		await ctx.send("Registeration failed. Ask a Koder for registration")
		mydb.close()