import logzero
import typer

from superhub import dispatcher, utils

logger = utils.init_logger()
app = typer.Typer(add_completion=False)


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
    trades: list[str] = typer.Option(
        [], '--trades', '-t', help='Trades to be scraped. Empty value implies all trades.'
    ),
    compress: bool = typer.Option(
        False, '--compress', '-x', show_default=False, help='Compress output data files.'
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)
    disp = dispatcher.Dispatcher()
    disp.scrap_all(filter=trades)
    if compress:
        disp.compress()


if __name__ == "__main__":
    app()
