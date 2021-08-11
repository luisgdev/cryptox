from os import getcwd, path
from tinydb import Query, TinyDB
from typing import List

import requests
import typer


class Cryptox:
    def __init__(self, symbol: str):
        self.url: str = 'https://api.coingecko.com/api/v3'
        self.symbol = symbol

    def _get_coin_list(self) -> List[dict]:
        endpoint: str = '/coins/list'
        response: List[dict] = requests.get(self.url + endpoint).json()
        return response

    def _get_price(self, ids: str, vs_currencies: str = 'usd,btc') -> dict:
        endpoint: str = '/simple/price'
        params: dict = {"ids": ids, "vs_currencies": vs_currencies}
        response: dict = requests.get(self.url + endpoint, params).json()
        return response[ids]

    def view_price(self, vs_pairs: str = 'usd,bnb,btc') -> None:
        symbol_found: bool = False
        db_item: List[dict] = db.search(Query().symbol == self.symbol)
        data: List[dict] = db_item if db_item else self._get_coin_list()
        for item in data:
            if self.symbol == item['symbol']:
                symbol_found = True
                print(f'.\nCoingecko ID: {item["id"]}')
                print(f'Token SYMBOL: {self.symbol.upper()} ({item["name"]})')
                price: dict = self._get_price(item["id"], vs_pairs)
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
    crypto.view_price(pair)
    typer.echo('Source: Coingecko.com')


if __name__ == "__main__":
    app()
