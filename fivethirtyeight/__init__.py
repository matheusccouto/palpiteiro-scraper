"""FiveThirtyEight Soccer Power Index scraper."""

import datetime
import logging
import os

import azure.functions as func

import helper

CONNECTION = os.environ["CONNECTION"]

NOW = datetime.datetime.now().isoformat()
CONTAINER = "fivethirtyeight"
BLOBS = {
    f"matches_latest/{NOW}.csv": "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches_latest.csv",
    f"global_rankings/{NOW}.csv": "https://projects.fivethirtyeight.com/soccer-api/club/spi_global_rankings.csv",
    f"global_rankings_intl/{NOW}.csv": "https://projects.fivethirtyeight.com/soccer-api/international/spi_global_rankings_intl.csv",
}

VERIFY_SSL = True


def main(timer: func.TimerRequest) -> None:
    """Main execution"""
    logging.info("Python timer trigger function ran at %s", datetime.datetime.now())

    if helper.game_over():
        logging.info("Game is over. Do not scrape.")
        return

    logging.info("Scrape data")
    helper.scrape(CONNECTION, CONTAINER, BLOBS, None, VERIFY_SSL)
    return
