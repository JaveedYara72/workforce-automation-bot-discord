# Manual file imports
import json
import discord
from discord.ext import commands, tasks
import asyncio
import requests

# Logging format
import logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

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

# Define command
@bot.command()
@commands.has_any_role("Koders")
async def define(msg, *args):
   
    word = args[0] # API REQUEST
    url = 'https://owlbot.info/api/v4/dictionary/' + str(word)
    headers = { "Authorization": CONFIG.OWL_TOKEN }
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("Something went wrong during requesting API. Reason: " + str(e)) # Request exception

    data = json.loads(response.text) # JSON PARSE WITH EMBED
    try:
        for i in range(0, len(data['definitions'])):
            embed=discord.Embed(title="Word: " + str(word), color=0x57b28f)
            embed.set_author(name="Kourage Word Analyzer", 
                    url="https://www.github.com/koders-in/kourage",
                    icon_url=bot.user.avatar_url)
            if data['definitions'][i]['image_url'] is not None:
                embed.set_thumbnail(url=data['definitions'][i]['image_url'])
            embed.add_field(name="Type",
                    value=data['definitions'][i]['type'],
                    inline=True)
            embed.add_field(name="Meaning",
                    value= "**" + data['definitions'][i]['definition'] + "**" ,
                    inline=False)
            if data['definitions'][i]['example'] is None:
                data['definitions'][i]['example'] = "N/A"
            embed.add_field(name="Example",
                    value= "_" + data['definitions'][i]['example'] + "_" ,
                    inline=False)
            embed.set_footer(text="Made with ❤️️  by Koders")
            await msg.send(embed=embed)
    except Exception as e:
        print("Something went wrong during parsing JSON. Reason: " + str(e)) # JSON parsing exception

# Vision command
@bot.command()
@commands.has_any_role("Kore")
async def vision(msg):
    await msg.message.delete()
    embed = EMBEDS.vision()
    await msg.send(embed=embed)

# Remind command
@bot.command()
@commands.has_any_role("Koders")
async def remind(msg, *args):
    await msg.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    embed = discord.Embed(title="Hello there! You have a reminder ^_^",
            color=0x57b28f)
    embed.add_field(name="Don't forget to:",
            value="{0}".format(args[1]),
            inline=False)
    embed.add_field(name="By yours truly :ghost:",
            value="Kourage",
            inline=False)
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2919/2919780.svg")
    embed.set_footer(text="Made with ❤️️  by Koders")
    await msg.send(embed=embed)
    msg = await msg.send(args[2])
    await msg.delete() # Deletes @person message who got tagged

# Poll command
@bot.command()
@commands.has_any_role('Koders')
async def poll(msg, question, *options: str):
    await msg.message.delete()
    embed=discord.Embed(title="Hello there! Please vote. ^_^",
            description=question,
            color=0x54ab8a)
    embed.set_author(name="Koders")
    reactions = [ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣' ]
    for _x, option in enumerate(options):
        embed.add_field(name=reactions[_x],
                value=option,
                inline=True)
    embed.set_footer(text="Made with ❤️️  by Koders")
    react_message = await msg.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)

if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)

