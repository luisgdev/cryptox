from tinydb import TinyDB, Query
import requests
import typer


# SETTINGS
app = typer.Typer()
db = TinyDB('symbols.json')


class Cryptox:
    def __init__(self, coin):
        self.url = 'https://api.coingecko.com/api/v3'
        self.db_path = 'coins.json'
        self.coin = coin

    def get_coin_list(self):
        endpoint = '/coins/list'
        response = requests.get(self.url + endpoint).json()
        return response

    def get_price(self, ids, vs_currencies):
        endpoint = f'/simple/price'
        params = {"ids": ids, "vs_currencies": vs_currencies}
        response = requests.get(self.url + endpoint, params=params).json()
        return response[ids]

    def get_coin_price(self):
        db_item = db.search(Query().symbol == self.coin)
        if db_item:
            data = db_item
        else:
            data = self.get_coin_list()
        for item in data:
            if self.coin == item['symbol']:
                print(f'.\nCoingecko ID: {item["id"]}')
                print(f'Token SYMBOL: {item["symbol"].upper()} ({item["name"]})')
                price = self.get_price(item["id"], "usd,btc")
                print(f' * USD value: {price["usd"]}')
                print(f' * BTC value: {price["btc"]}')
                if not db_item:
                    db.insert(item)


@app.command()
def main(name: str):
    crypto = Cryptox(name)
    typer.echo(crypto.get_coin_price())
    typer.echo('Source: Coingecko.com')


if __name__ == "__main__":
    app()
