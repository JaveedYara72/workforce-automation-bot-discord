import discord
from discord.ext import commands, tasks
import asyncio

# LOGGING WITH FORMAT
import logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

# Manual file imports
import config as CONFIG # Capitals for global
import embeds as EMBEDS 

bot = commands.Bot(command_prefix="&")

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

# Remind command
@bot.command()
@commands.has_any_role("Koders")
async def remind(ctx, *args):
    await ctx.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    author = ctx.author.name
    embed = discord.Embed(title="{0}".format(args[1]), color=0x2459bc)
    embed.set_author(name="Auto Reminder!")
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2919/2919780.svg")
    embed.add_field(name="Invoked by ", value="{0}".format(author), inline=True)
    embed.add_field(name="Invoked for ", value="{0}".format(args[2]), inline=True)
    embed.set_footer(text="Made with ❤️️  by Koders")
    await ctx.send(embed=embed)
    msg = await ctx.send(args[2])
    await msg.delete()




if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as e:
        logging.warning("Exception found at main worker", exc_info=True)

    
