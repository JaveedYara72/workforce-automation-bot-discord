import discord
import mysql.connector
import settings as setting


async def add(ctx, assigned_to):

	mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)
	mycur = mydb.cursor(buffered=True)

	def update(update_query, value):
		mycur.execute(update_query, value)
		mydb.commit()

	try:
		total_xp = 0
		mycur.execute("select Given_XP from task where Assigned_To = %s", (assigned_to, ))
		for row in mycur:
			total_xp = row[0] + total_xp


		mycur.execute("select Level from internal where Discord_Username = %s", (assigned_to, ))
		row = mycur.fetchone()
		start_level = row[0]
		end_level = int((total_xp)**(1/4))



		update_query = "update internal set Total_XP = %s where Discord_Username = %s"
		value = (total_xp, assigned_to)
		update(update_query, value)

		if start_level < end_level:
			level = end_level
			update_query = "update internal set Level = %s where Discord_Username = %s"
			value = (level, assigned_to)
			update(update_query, value)
		await ctx.send("Task completed.")
	except Exception as error:
		await ctx.send("You are not registered as Koders")