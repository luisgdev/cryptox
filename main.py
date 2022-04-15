"""
Main file for Cryptox
"""

from os import getcwd, path
from typing import List

import requests
import typer
from pydantic import BaseModel
from tinydb import Query, TinyDB

from models import Cryptox

# SETTINGS
app = typer.Typer()
db = TinyDB(path.join(getcwd(), "symbols.json"))


@app.command()
def main(symbol: str, vs: str = "usd", n: float = 0):
    crypto = Cryptox(symbol)
    crypto.view_price(vs, n)
    typer.echo("Source: Coingecko.com")


if __name__ == "__main__":
    app()
