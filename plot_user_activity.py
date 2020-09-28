import discord
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv


async def plot_user_activity(client, ctx):
    plt.style.use('fivethirtyeight')
    df = pd.read_csv('innovators.csv', encoding= 'unicode_escape')

    author = df['author'].to_list()

    message_counter = {}

    for i in author:
        if i in message_counter:
            message_counter[i] += 1
        else:
            message_counter[i] = 1
    
    # for not mentioning the bot in the line graph. 
    message_counter.pop('ninza_bot_test')
    
    authors_in_discord = list(message_counter.keys())
    no_of_messages = list(message_counter.values())

    plt.plot(authors_in_discord, no_of_messages, marker = 'o', markersize=10)
    plt.title('msg sent by author in the server.')
    plt.xlabel('Author')
    plt.ylabel('Message_count')

    plt.savefig('output2.png')
    plt.tight_layout()
    plt.close()

    await ctx.send(file = discord.File('output2.png'))
