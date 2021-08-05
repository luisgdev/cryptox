from os import path, getcwd
from tinydb import TinyDB, Query
import requests
import typer


class Cryptox:
    def __init__(self, symbol: str):
        self.url: str = 'https://api.coingecko.com/api/v3'
        self.symbol: str = symbol

    def _get_coin_list(self) -> list:
        endpoint: str = '/coins/list'
        response: list = requests.get(self.url + endpoint).json()
        return response

    def _get_price(self, ids: str, vs_currencies: str = 'usd,btc') -> dict:
        endpoint: str = f'/simple/price'
        params: dict = {"ids": ids, "vs_currencies": vs_currencies}
        response: dict = requests.get(self.url + endpoint, params=params).json()
        return response[ids]

    def view_price(self, vs_pairs: str = 'usd,bnb,btc') -> None:
        symbol_found: bool = False
        db_item: list = db.search(Query().symbol == self.symbol)
        if db_item:
            data: list = db_item
        else:
            data: list = self._get_coin_list()
        for item in data:
            if self.symbol == item['symbol']:
                symbol_found = True
                print(f'.\nCoingecko ID: {item["id"]}')
                print(f'Token SYMBOL: {self.symbol.upper()} ({item["name"]})')
                price = self._get_price(item["id"], vs_pairs)
                for key in price.keys():
                    print(f' * {key.upper()} value: {price[key]}')
                if not db_item:
                    db.insert(item)
        if not symbol_found:
            print(f'Error: Symbol {self.symbol.upper()} not found.')


# SETTINGS
app = typer.Typer()
db = TinyDB(path.join(getcwd(), 'symbols.json'))

@app.command()
def main(name: str, pair: str = 'usd'):
    crypto = Cryptox(name)
    typer.echo(crypto.view_price(pair))
    typer.echo('Source: Coingecko.com')


if __name__ == "__main__":
    app()
