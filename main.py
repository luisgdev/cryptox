"""
Main file for Cryptox
"""

import typer

from models import Cryptox

app = typer.Typer()


@app.command()
def main(symbol: str, pairs: str = "USD,EUR", amount: float = 0) -> None:
    """
    Main function.
    :param symbol: Cryptocurrency symbol.
    :param pairs: Pair to compare cryptocurrency value.
    :param amount: Amount of cryptocurrencies to calculate value.
    :return: None
    """
    crypto = Cryptox(symbol)
    crypto.view_price(pairs, amount)
    typer.echo("Source: Coingecko.com")


if __name__ == "__main__":
    app()
