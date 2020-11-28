import discord
from discord.ext import commands, tasks
import asyncio

# LOGGING WITH FORMAT
import logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

# Manual file imports
import config as CONFIG # Capitals for global

bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():
    logging.info("Kourage is running at version {0}".format(CONFIG.VERSION))

if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as e:
        logging.error("MAIN RUN EXCEPTION", exc_info=True)

    
