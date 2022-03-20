from os import getcwd, path
from tinydb import Query, TinyDB
from typing import List
from pydantic import BaseModel

import requests


# SETTINGS
db = TinyDB(path.join(getcwd(), "symbols.json"))

COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
SIMPLE_PRICE_ENDPOINT: str = "/simple/price"
COIN_LIST_ENDPOINT: str = "/coins/list"


class Token(BaseModel):
    """
    Details for a crypto token
    """

    id: str
    name: str
    symbol: str


class Cryptox:
    """
    Cryptocurrency price from Coingecko.
    Usage:
        python main.py <token> --pair usd,btc
        python main.py <token> --amount 0.5
    """

    def __init__(self: "Cryptox", symbol: str) -> None:
        self.url: str = COINGECKO_API_URL
        self.symbol = symbol

    def _get_coin_list(self: "Cryptox") -> List[dict]:
        response: List[dict] = requests.get(
            self.url + COIN_LIST_ENDPOINT
        ).json()
        return response

    def _get_price(
        self: "Cryptox", id: str, vs_currencies: str = "usd,btc"
    ) -> dict:
        params: dict = {"ids": id, "vs_currencies": vs_currencies}
        response: dict = requests.get(
            self.url + SIMPLE_PRICE_ENDPOINT, params
        ).json()
        return response[id]

    def view_price(self, vs_pairs: str = "usd,btc", amount: float = 0) -> None:
        symbol_found: bool = False
        db_item: List[dict] = db.search(Query().symbol == self.symbol)
        data: List[dict] = db_item if db_item else self._get_coin_list()
        for item in data:
            token = Token(**item)
            if self.symbol == token.symbol:
                symbol_found = True
                print(f".\nCoingecko ID: {token.id}")
                print(f"Token SYMBOL: {token.symbol.upper()} ({token.name})")
                price: dict = self._get_price(token.id, vs_pairs)
                for key in price.keys():
                    # Here You can save the price for calculations.
                    print(f" * {key.upper()} value: {price[key]}")
                    if amount:
                        conv: float = round(amount * price[key], 4)
                        print(f"  * {amount} {token.symbol} = {conv} {key} ")
                if not db_item:
                    db.insert(item)
        if not symbol_found:
            print(f"Error: Symbol {self.symbol.upper()} not found.")