import requests
from flask import Flask,request
from markupsafe import escape
import db
import generator_api_routes
import datetime
app = Flask(__name__)

global sleep_api

sleep_api = None

def search_coin(id_coin='BTC'):
    request = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/lite?id={id_coin}')
    if request.status_code == 200:
        response = request.json()
    else:
        print('requisição falhou')

    response['data']['timestamp'] = response['status']['timestamp']
    return response,request.status_code


def tratament_response(response):
    data = {}
    data['name'] = response[0]['response']['data']['name']
    data['symbol'] = response[0]['response']['data']['symbol']
    data['timestamp'] = response[0]['response']['data']['timestamp']
    data['price'] = response[0]['response']['data']['statistics']['price']
    data_to_insert,placeholders,columns = tratament_columns_and_placeholders(data)
    return data_to_insert,placeholders,columns

def tratament_columns_and_placeholders(data):
    columns = ','.join(data.keys())
    data_to_insert = tuple(data.values())
    placeholders =  ','.join(['?' for a in range(len(data_to_insert))])
    return data_to_insert,placeholders,columns

def validation_many_requests(sleep_api):
    if sleep_api:
        if datetime.datetime.now() < sleep_api + datetime.timedelta(seconds=30):
            return False
        else:
            return True
    return True


@app.route('/coins/<coin>',methods=['GET'])
def coin(coin):
        global sleep_api
        validation = validation_many_requests(sleep_api)
        if validation:
            coins_api_route = generator_api_routes.generator_coins_route()
            id_coin = coins_api_route[coin.upper()]
            status = {'status':200}
            try:
                response,status_code = search_coin(id_coin)
            except Exception as e:
                status = {'status':status_code,'erro':e}
            response_request = [{'response':response},{'status_requests':status}]
            data_to_insert,placeholders,columns = tratament_response(response_request)
            db.insert_table('requisicao',placeholders,columns,data_to_insert)
            sleep_api = datetime.datetime.now()
            return response_request
        else:
            return 'Aguarde um momento'
    

if __name__ == '__main__':
    app.run(debug=True)