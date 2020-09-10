import discord
from discord.ext import commands
import sqlite3

###############################################################################################################
# MANUAL IMPORT
###############################################################################################################
import settings as setting


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

def delete(delete_query, value):
	mycur.execute(delete_query, value)
	mydb.commit()



###############################################################################################################
# SUGGESTION
###############################################################################################################
async def suggestion(client, ctx, title, description):

	embed = discord.Embed(title=title, colour = discord.Colour.blue())

	username = ctx.message.author.name
	insert_query = "insert into suggestion(author, title, description) values(?, ?, ?)"
	value = (username, title, description)

	insert(insert_query, value)

	mycur.execute("select * from suggestion order by number desc limit 1;")
	row = mycur.fetchone()
	number = row[1]


	embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	embed.add_field(name='suggestion #{}'.format(number), value=description)
	embed.set_footer(text="Made by Koders Dev")
	await ctx.send(embed=embed)

	channel = client.get_channel(setting.SUGGESTIONS)
	await channel.send(embed=embed)



###############################################################################################################
# REPLY SUGGESTION
###############################################################################################################
async def reply_suggestion(client, ctx, number, is_considered, reason):

	try:
		mycur.execute("select author, description, title from suggestion where number = ?", (number, ))
		row = mycur.fetchone()
		author = row[0]
		description = row[1]
		title = row[2]

		embed = discord.Embed(title=title, colour = discord.Colour.blue())
		username = ctx.message.author.name

		if is_considered == 1:
			update_query = "update suggestion set reason = ?, is_considered = ?, considered_by = ? where number = ?"
			value = (reason, is_considered, username, number)
			update(update_query, value)


			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(ctx.author), value=reason, inline=False)
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

			channel = client.get_channel(setting.CONSIDERED_SUGGESTIONS)
			await channel.send(embed=embed)

		elif is_considered == 2:
			update_query = "update suggestion set reason = ?, is_considered = ?, considered_by = ? where number = ?"
			value = (reason, is_considered, username, number)
			update(update_query, value)


			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} not considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(ctx.author), value=reason)
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

			channel = client.get_channel(setting.SUGGESTIONS)
			await channel.send(embed=embed)
	

	except Exception as e:
		await ctx.send("error occured = {}".format(e))
	


###############################################################################################################
# DISPLAY SUGGESTION
###############################################################################################################

async def display(client, ctx, number):
	try:
		mycur.execute("select * from suggestion where number = ?", (number, ))
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
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

		elif is_considered == 1:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(considered_by), value=reason)
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

		elif is_considered == 2:
			embed.set_author(name=author)
			embed.add_field(name='suggestion #{} not considered'.format(number), value=description, inline=False)
			embed.add_field(name='Reason from {}'.format(considered_by), value=reason)
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

		else:
			await ctx.send("The suggesion number does not exit.")
	
	except Exception as e:
		await ctx.send("Command ivoke error occur check your command again.")
	


###############################################################################################################
# DELETING SUGGESTION
###############################################################################################################

async def delete_suggestion(client, ctx, number):
	try:
		mycur.execute("select * from suggestion where number = ?", (number, ))
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
			embed.set_footer(text="Made by Koders Dev")
			await ctx.send(embed=embed)

		delete_query = "delete from suggestion where number = ?"
		value = (number, )
		delete(delete_query, value)


		await ctx.send("suggestion #{} deleted from database".format(number))
	
	except Exception as e:
		await ctx.send("The exception occur while deleting a record.")

