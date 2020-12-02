import discord
from discord.ext import commands, tasks
import asyncio

# Logging format
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

# Remind command
@bot.command()
@commands.has_any_role("Koders")
async def remind(ctx, *args):
    await ctx.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    author = ctx.author.name
    embed = discord.Embed(title="Hello there! You have a reminder ^_^", color=0x57b28f)
    embed.add_field(name="Don't forget to:", value="{0}".format(args[1]), inline=False)
    embed.add_field(name="By yours truly :sunflower:", value="Kourage", inline=False)
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2919/2919780.svg")
    embed.set_footer(text="Made with ❤️️  by Koders")
    await ctx.send(embed=embed)
    msg = await ctx.send(args[2])
    await msg.delete() # Deletes @person message who got tagged

# Poll command
@bot.command()
@commands.has_any_role('Koders')
async def poll(ctx, question, *options: str):
    embed = discord.Embed(
            title = question, 
            color = discord.Colour.blue()
            )
    reactions = [ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣' ]
    description = []
    for x, option in enumerate(options):
        description += '\n {} {} \n'.format(reactions[x], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)

if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as e:
        logging.warning("Exception found at main worker", exc_info=True)

    
