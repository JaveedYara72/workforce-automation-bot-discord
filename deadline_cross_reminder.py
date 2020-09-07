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


async def add(ctx, task_id):

	mydb = mysql.connector.connect(host=setting.HOST, port=setting.PORT, database=setting.DATABASE, user=setting.USER, password=setting.PASSWORD)
	mycur = mydb.cursor(buffered=True)


	mycur.execute("select * from task where Id = %s", (task_id, ))
	row = mycur.fetchone()
	task_id = row[0]
	title = row[1]
	description = row[2]
	assigned_to = row[3]
	assigned_by = row[4]
	status = row[5]
	estimated_time = row[6]
	estimated_xp = row[8]
	project_id = row[10]


	if status == "In_Progress":
		embed = discord.Embed(title="Deadline Cross Reminder", 
			description="{} You have not Completed your task on time.".format(assigned_to))
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


	mydb.close()