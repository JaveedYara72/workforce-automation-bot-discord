import discord
import asyncio
import gsheets
import settings as setting
async def worklog(client, ctx):
    inputs = []
    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel

    def check(reaction, user):
        return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author

    def check_role_management(reaction, user):
        return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and str(user) != "Cypher#5959"

    async def take_input():
        try:
            message = await client.wait_for('message', check=pred, timeout=44.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Try again later.")
        else:
            return message

    async def take_reaction_management():
        try:
            result = await client.wait_for('reaction_add', check=check_role_management, timeout=15000.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Try again later.")
        else:
            reaction, user = result
            if (str(reaction.emoji) == '☑'):
                return True
            if (str(reaction.emoji) == '❎'):
                return False

    async def take_reaction():
        try:
            result = await client.wait_for('reaction_add', check=check, timeout=44.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Try again later.")
        else:
            reaction, user = result
            if (str(reaction.emoji) == '☑'):
                return True
            if (str(reaction.emoji) == '❎'):
                return False

    # Embed for work title
    embed = discord.Embed(title="Hello there! (0/2)",
                          description="Let's log your work!.\n\nPlease enter what you have worked on!")
    embed.set_author(name="Welcome to Koders | Efficiency Management",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
    embed.set_footer(text="Example\nWorked on Integrity for making efficiency management")
    textEmbed = await ctx.send(embed=embed)
    textInput = await take_input()
    inputs.append(textInput.content)
    await textInput.delete()
    await textEmbed.delete()

    # Embed for working hours
    embed = discord.Embed(title="Great, next step! (1/2)",
                          description="Please enter number of hours\n(you won't put unreasonable time, pinky promise!?)")
    embed.set_author(name="Welcome to Koders | Efficiency Management",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")
    embed.set_footer(text="Example\n45 mins")
    textEmbed = await ctx.send(embed=embed)
    textInput = await take_input()
    inputs.append(textInput.content)
    await textInput.delete()
    await textEmbed.delete()

    # Embed for under process
    embed = discord.Embed(title="Rest now! (2/2)",
                          description="Your work log is under process.\n\nPlease rest.")
    embed.set_author(name="Welcome to Koders | Registration",
                     icon_url="https://cdn.discordapp.com/attachments/700257704723087359/709710821382553640/K_with_bg_1.png")


    print(inputs)
    # Embed for confirmation to management
    embed = discord.Embed(title="Confirmation", description="Please recheck the information and type yes or no",
                          color=0x0e71c7)
    embed.set_author(name="Are you sure?", url="https://www.github.com/koders-in/integrity",
                     icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://image-1.flaticon.com/icons/png/32/2921/2921124.png")
    embed.add_field(name="Work title", value=inputs[0], inline=False)
    embed.add_field(name="Working hours", value=inputs[1], inline=False)
    to_channel = client.get_channel(setting.WORK_LOGGED)
    text = await to_channel.send(embed=embed)

    userclient = await text.add_reaction(emoji="☑")
    await text.add_reaction(emoji="❎")

    result = await take_reaction_management()
    print(result)
    await text.delete()
    if (result):
        to_channel = client.get_channel(setting.EFFICIENCY_MANAGEMENT)
        response = gsheets.insert(ctx.author.name, inputs[0], inputs[1])
        embed = discord.Embed(title="Great work! Here are the details of your log")
        embed.set_author(name="Work Logged!")
        embed.add_field(name="Log id", value=response[0], inline=True)
        embed.add_field(name="Work title", value=response[2], inline=True)
        embed.add_field(name="Time taken", value=response[3], inline=True)
        embed.add_field(name="Done by", value=response[4], inline=True)
        embed.set_footer(text="Logged at " + response[1])
        await to_channel.send(embed=embed)
    else:
        await ctx.send("Work logging rejected. Please contact management.")
