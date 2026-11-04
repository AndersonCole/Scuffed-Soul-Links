import requests

trade = requests.get('https://pokeapi.co/api/v2/encounter-condition/15/').json()

test= ''
for method in trade['values']:
    test+= f'\'{method["name"]}\', '

print(test)