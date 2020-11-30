import discord
from discord.ext import commands, tasks
import asyncio

# LOGGING WITH FORMAT
import logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

# Manual file imports
import config as CONFIG # Capitals for global
import embeds as EMBEDS 

bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready(): # Triggers when bot is ready
    logging.info("Kourage is running at version {0}".format(CONFIG.VERSION))

# Ping command
@bot.command()
@commands.has_any_role("@everyone")
async def ping(msg):
    await msg.send('Pong! 🏓\n ' + 
              'Name: Kourage \n ' +
              'Description: AIO bot of Koders \n ' +
              'Version: {0} \n '.format(CONFIG.VERSION) +
              'Username: {0} \n '.format(msg.author.name) +
              'Latency: {0} sec '.format(round(bot.latency, 1)))

# Vision command
@bot.command()
@commands.has_any_role("Kore")
async def vision(msg):
    embed = EMBEDS.vision()
    await msg.send(embed=embed)

if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as e:
        logging.warning("Exception found at main worker", exc_info=True)

    
