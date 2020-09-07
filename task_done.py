import discord
import mysql.connector
import settings as setting
import asyncio

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################

import email_template as EMAIL_TEMPLATE
import leveling_system as LEVEL_SYSTEM
import dm_template as DM_TEMPLATE


async def add(client, ctx, task_id):

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
	embed.add_field(name="Time_Taken", value=inputs[0], inline=False)
	embed.add_field(name="Given_XP", value=inputs[1], inline=False)
	embed.add_field(name="Status", value=inputs[2], inline=True)

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
		insert_query = "update task set Time_Taken = %s, Given_XP = %s, Status = %s where Id = %s"
		value = (time_taken, given_xp, status, task_id)
		insert(insert_query, value)

		mycur.execute("select * from task where id = %s", (task_id, ))
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
			embed.add_field(name="Description", value=description, inline=False)
			embed.add_field(name="Assigned_To", value=assigned_to, inline=True)
			embed.add_field(name="Assigned_By", value=assigned_by, inline=True)
			embed.add_field(name="Status", value=status, inline=False)
			embed.add_field(name="Estimated_Time", value=estimated_time, inline=True)
			embed.add_field(name="Time_Taken", value=time_taken, inline=True)
			embed.add_field(name="Estimated_XP", value=estimated_xp, inline=False)
			embed.add_field(name="Given_XP", value=given_xp, inline=True)
			embed.add_field(name="Project_Id", value=project_id, inline=False)

			accepted_task_channel = client.get_channel(setting.ACCEPTED_TASK_CHANNEL_ID)

			await accepted_task_channel.send(embed=embed)

		await LEVEL_SYSTEM.add(ctx, assigned_to)