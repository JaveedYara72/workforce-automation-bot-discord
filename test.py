import requests

url = 'https://owlbot.info/api/v4/dictionary/fruit salad' 
headers = { "Authorization": "Token c5a6932805bff0c739cd87d45dd8530d88c064bd" }
try:
    response = requests.get(url, headers=headers)
except Exception as e:
    print("Something went wrong: " + e)
print(response.text)
