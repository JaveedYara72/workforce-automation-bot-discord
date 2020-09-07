import discord
from discord.ext import commands
import mysql.connector

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################

import settings as setting


###############################################################################################################
# SUGGESTION
###############################################################################################################

async def suggestion(ctx, title, description):
	mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)
	mycur = mydb.cursor(buffered=True)

	def insert(insert_query, value):
		mycur.execute(insert_query, value)
		mydb.commit()

	embed = discord.Embed(title=title, colour = discord.Colour.blue())

	username = ctx.message.author.name
	insert_query = "insert into suggestion(author, title, description) values(%s, %s, %s)"
	value = (username, title, description)

	insert(insert_query, value)

	mycur.execute("select * from suggestion order by number desc limit 1;")
	row = mycur.fetchone()
	number = row[1]


	embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	embed.add_field(name='suggestion #{}'.format(number), value=description)
	await ctx.send(embed=embed)
	mydb.close()

###############################################################################################################
# REPLY SUGGESTION
###############################################################################################################

async def reply_suggestion(ctx, number, is_considered, reason):

	try:
		mydb = mysql.connector.connect(host="localhost", user="root", password="", database="ticket")
		mycur = mydb.cursor(buffered=True)

		def update(update_query, value):
			mycur.execute(update_query, value)
			mydb.commit()

		mycur.execute("select author, description, title from suggestion where number = %s", (number, ))
		row = mycur.fetchone()
		author = row[0]
		description = row[1]
		title = row[2]

		reply_embed = discord.Embed(title=title, colour = discord.Colour.blue())
		username = ctx.message.author.name

		if is_considered == 1:
			update_query = "update suggestion set reason = %s, is_considered = %s, considered_by = %s where number = %s"
			value = (reason, is_considered, username, number)
			update(update_query, value)


			reply_embed.set_author(name=author)
			reply_embed.add_field(name='suggestion #{} considered'.format(number), value=description, inline=False)
			
			reply_embed.add_field(name='Reason from {}'.format(ctx.author), value=reason, inline=False)
			await ctx.send(embed=reply_embed)

		elif is_considered == 2:
			update_query = "update suggestion set reason = %s, is_considered = %s, considered_by = %s where number = %s"
			value = (reason, is_considered, username, number)
			update(update_query, value)


			reply_embed.set_author(name=author)
			reply_embed.add_field(name='suggestion #{} not considered'.format(number), value=description, inline=False)		

			reply_embed.add_field(name='Reason from {}'.format(ctx.author), value=reason)
			await ctx.send(embed=reply_embed)
		mydb.close()

	except Exception as e:
		await ctx.send("error occured = {}".format(e))
		mydb.close()


###############################################################################################################
# DISPLAY SUGGESTION
###############################################################################################################

async def display(ctx, number):
	try:
		mydb = mysql.connector.connect(host="localhost", user="root", password="", database="ticket")
		mycur = mydb.cursor(buffered=True)
		
		mycur.execute("select * from suggestion where number = %s", (number, ))
		row = mycur.fetchone()
		author = row[0]
		number = row[1]
		title = row[2]
		description = row[3]
		reason = row[4]
		is_considered = row[5]
		considered_by = row[6]

		embed = discord.Embed(title=title, colour = discord.Colour.blue())
		if is_considered == 0:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{}'.format(number), value=description, inline=False)
			await ctx.send(embed=embed)
		elif is_considered == 1:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(considered_by), value=reason)
			await ctx.send(embed=embed)
		elif is_considered == 2:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} not considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(considered_by), value=reason)
			await ctx.send(embed=embed)
		else:
			await ctx.send("The suggesion number does not exit.")
		mydb.close()
	except Exception as e:
		await ctx.send("Command ivoke error occur check your command again.")
		mydb.close()


###############################################################################################################
# DELETING SUGGESTION
###############################################################################################################

async def delete_suggestion(ctx, number):
	try:
		mydb = mysql.connector.connect(host="localhost", user="root", password="", database="ticket")
		mycur = mydb.cursor(buffered=True)

		def delete(delete_query, value):
			mycur.execute(delete_query, value)
			mydb.commit()
		
		mycur.execute("select * from suggestion where number = %s", (number, ))
		row = mycur.fetchone()
		author = row[0]
		number = row[1]
		title = row[2]
		description = row[3]
		reason = row[4]
		is_considered = row[5]
		considered_by = row[6]

		if is_considered == 2:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} not considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(considered_by), value=reason)
			await ctx.send(embed=embed)

		delete_query = "delete from suggestion where number = %s"
		value = (number, )
		delete(delete_query, value)


		await ctx.send("suggestion #{} delete from database".format(number))
		mydb.close()
	except Exception as e:
		await ctx.send("The exception occur while deleting a record.")
		mydb.close()
