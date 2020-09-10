import discord
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
def update(update_query, value):
	mycur.execute(update_query, value)
	mydb.commit()

###############################################################################################################
# LEVEL SYSTEM
###############################################################################################################
async def add(ctx, assigned_to):

	try:
		total_xp = 0
		mycur.execute("select Given_XP from task where Assigned_To = ?", (assigned_to, ))
		for row in mycur:
			total_xp = row[0] + total_xp


		mycur.execute("select Level from internal where Discord_Username = ?", (assigned_to, ))
		row = mycur.fetchone()
		start_level = row[0]
		end_level = int((total_xp)**(1/4))



		update_query = "update internal set Total_XP = ? where Discord_Username = ?"
		value = (total_xp, assigned_to)
		update(update_query, value)

		if start_level < end_level:
			level = end_level
			update_query = "update internal set Level = ? where Discord_Username = ?"
			value = (level, assigned_to)
			update(update_query, value)
		await ctx.send("Task completed.")
	except Exception as error:
		await ctx.send("You are not registered as Koders")