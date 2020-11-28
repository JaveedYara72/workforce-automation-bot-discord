import discord
from discord.ext import commands, tasks
import asyncio
import logging

# Manual file imports
import config as CONFIG # Capitals for global

bot = commands.Bot(command_prefix="&")

@bot.event
async def on_ready():
    logging.info("Kourage is running at version {0}".format(CONFIG.VERSION))

bot.run(CONFIG.TOKEN)
    
