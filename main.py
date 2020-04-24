import requests
import time

# SETTINGS
url = 'https://api.coingecko.com/api/v3'


def get_market_cap():
    endpoint = '/global'
    # REQUEST DATA
    data = requests.get(url + endpoint).json()
    result = data['data']['total_market_cap']['usd']
    return result


def get_coin_list():
    endpoint = '/coins/list'
    # REQUEST DATA
    data = requests.get(url + endpoint).json()
    result = data
    return result


def get_price(coin, vs_currencies):
    endpoint = f'/simple/price?ids={coin}&vs_currencies={vs_currencies}'
    # REQUEST DATA
    data = requests.get(url + endpoint).json()
    result = data[coin][vs_currencies]
    return result


def get_coin_price(symbol):
    data = get_coin_list()
    for item in data:
        if symbol == item['symbol']:
            print(f'{item["name"]} ({item["symbol"].upper()})')
            print(f'USD {get_price(item["id"], "usd")}')
            print(f'BTC {get_price(item["id"], "btc")}')


def main():
    get_coin_price(input('COIN: '))


if __name__ == "__main__":
    # Start counting elapsed time
    init_time = time.perf_counter()
    main()
    # Stopt counting elapsed time
    elapsed = round(time.perf_counter() - init_time, 2)
    print(f' *** Elapsed time: {elapsed} s ***\n.')