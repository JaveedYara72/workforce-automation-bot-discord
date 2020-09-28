import discord

async def dm_koders(author):
	await author.send("Thank you for showing interest at Koders.")

async def dm_community(author):
	await author.send("Thank you for showing interest at Koders. You are registered as community")

async def dm_client(author):
	await author.send("Thank you for showing interest at Koders. You are now our client")

async def dm_career(author):
	await author.send("Thank you for showing interest at Koders. You can begin career at Koders")

async def dm_partner(author):
	await author.send("Thank you for showing interest at Koders. You are now partner with Koders")

async def dm_project(author):
	await author.send("Thank you for showing interest at Koders. Your project has been registerd.")
