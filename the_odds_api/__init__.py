"""The Odds API scraper."""

import datetime
import logging
import os

import azure.functions as func

import helper

CONNECTION = os.environ["CONNECTION"]
THE_ODDS_API_KEY = os.environ["THE_ODDS_API_KEY"]

NOW = datetime.datetime.utcnow().isoformat()
CONTAINER = "the-odds-api"
BLOBS = {
    f"soccer_brazil_campeonato/{NOW}.json": f"https://api.the-odds-api.com/v4/sports/soccer_brazil_campeonato/odds/?apiKey={THE_ODDS_API_KEY}&regions=uk,eu&markets=h2h,spreads,totals",
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
