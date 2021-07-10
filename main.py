import requests
import time

# SETTINGS
url = 'https://api.coingecko.com/api/v3'


def get_market_cap():
    endpoint = '/global'
    # REQUEST DATA
    response = requests.get(url + endpoint).json()
    return response['data']['total_market_cap']['usd']


def get_coin_list():
    endpoint = '/coins/list'
    # REQUEST DATA
    response = requests.get(url + endpoint).json()
    return response


def get_price(coin, vs_currencies):
    endpoint = f'/simple/price'
    params = {"ids": coin, "vs_currencies": vs_currencies}
    # REQUEST DATA
    response = requests.get(url + endpoint, params=params).json()
    return response[coin][vs_currencies]


def get_coin_price(symbol):
    data = get_coin_list()
    for item in data:
        if symbol == item['symbol']:
            print(f'ID: {item["id"]}')
            print(f'{item["name"]} ({item["symbol"].upper()})')
            print(f'USD {get_price(item["id"], "usd")}')
            print(f'BTC {get_price(item["id"], "btc")}')


def main():
    print(f'Crypto Market Cap.: USD {round(get_market_cap(), 2)}')
    get_coin_price(input('COIN: '))
    print('Source: Coingecko.com')


if __name__ == "__main__":
    # Start counting elapsed time
    init_time = time.perf_counter()
    # Do the thing
    main()
    # Stop counting elapsed time
    elapsed = round(time.perf_counter() - init_time, 2)
    # Show elapsed time
    print(f' *** Elapsed time: {elapsed} s ***\n.')