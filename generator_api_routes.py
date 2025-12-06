import json


with open('coins.json',encoding='utf-8') as file:
    coins = json.load(file)


def generator_coins_route():
    coins_api_route = {}
    for coin in coins:
        coins_api_route[coin['symbol']] = coin['id']

    with open('coins_route.json', encoding='utf-8',mode='w') as file:
        file.write(json.dumps(ensure_ascii=True,indent=4,obj=coins_api_route))
    return coins_api_route

