import json

def generator_coins_route():
    with open('coins.json',encoding='utf-8') as file:
        coins = json.load(file)
    coins_api_route = {}
    for coin in coins:
        coins_api_route[coin['symbol']] = coin['id']
    return coins_api_route

