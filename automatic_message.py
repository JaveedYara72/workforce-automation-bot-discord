import discord
from discord.ext import commands
import asyncio
from datetime import datetime

TOKEN = "real_token"
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	print("Bot is ready.")


def __datetime(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')



async def background_task():
    await client.wait_until_ready()

    channel = client.get_channel(735072906702225426) # Insert channel ID here
    while not client.is_closed():

    	embed = discord.Embed(
    		title = "opening and closing time is 11:00 AM and 6:00 PM"
    	)
    	embed.set_author(name='Welcome to Koders', icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
    	now = datetime.now()
    	current_time = now.strftime("%H:%M:%S")
    	set_time1 = "11:24:00"
    	set_time2 = "11:26:00"
    	start1 = __datetime(current_time)
    	end1 = __datetime(set_time1)
    	end2 = __datetime(set_time2)
    	delta1 = end1 - start1
    	delta2 = end2 - start1
    	delay1 = delta1.total_seconds()
    	delay2 = delta2.total_seconds()

    	while current_time != set_time1:
    		if delay1 > 0:
    			await asyncio.sleep(delay1)
    			await channel.send(embed=embed)
    		break

    	while current_time != set_time2:
    		if delay2 > 0:
    			await asyncio.sleep(delay2)
    			await channel.send(embed=embed)
    		break


client.loop.create_task(background_task())
client.run(TOKEN)
