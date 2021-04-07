import requests
import json

# TODO 
# CUSTOM NAMING
# EMBED 

# API REQUEST
word = 'salad'
url = 'https://owlbot.info/api/v4/dictionary/' + word
headers = { "Authorization": "Token c5a6932805bff0c739cd87d45dd8530d88c064bd" }
try:
    response = requests.get(url, headers=headers)
except Exception as e:
    print("Something went wrong during requesting API. Reason: " + e)

# PARSE JSON
# print(response.text)
data = json.loads(response.text)
try:
    # print(len(data['definitions']))
    # print(data['definitions'])
    for i in range(0, len(data['definitions'])):
        print(data['definitions'][i]['type'])
        print(data['definitions'][i]['definition'])
        print(data['definitions'][i]['example'])
        print(data['definitions'][i]['image_url'])
        print(data['definitions'][i]['emoji'])
except Exception as e:
    print("Something went wrong during parsing JSON. Reason: " + e)

#embed=discord.Embed(title="Koolz! Here is my analysis ^_^", color=0x57b28f)
#embed.set_author(name="Kourage Word Analyzer", url="https://www.github.com/koders-in/kourage", icon_url="https://media.owlbot.info/dictionary/images/ggggggggggggggggs.jpg.400x400_q85_box-131,0,669,539_crop_detail.jpg")
#embed.set_thumbnail(url="https://media.owlbot.info/dictionary/images/ggggggggggggggggs.jpg.400x400_q85_box-131,0,669,539_crop_detail.jpg")
#embed.add_field(name="Type", value="Bold", inline=True)
#embed.add_field(name="Emoji", value="Emoji", inline=True)
#embed.add_field(name="Meaning", value="Regular", inline=False)
#embed.add_field(name="Example", value="Italic", inline=False)
#embed.set_footer(text="Made with :heart:  by Koders")
#await ctx.send(embed=embed)
