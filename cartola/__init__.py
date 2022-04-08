"""Cartola FC scraper."""

import datetime
import logging
import os

import azure.functions as func
import requests

import helper

CONNECTION = os.environ["CONNECTION"]
USERNAME = os.environ["GLOBO_USERNAME"]
PASSWORD = os.environ["GLOBO_PASSWORD"]
GLBID = os.environ["GLBID"]

NOW = datetime.datetime.now().isoformat()
HEADERS = {"X-GLB-Token": GLBID}
CONTAINER = "cartola"
BLOBS = {
    f"mercado/status/{NOW}.json": "https://api.cartola.globo.com/mercado/status",
    f"mercado/destaques/{NOW}.json": "https://api.cartola.globo.com/mercado/destaques",
    f"patrocinadores/{NOW}.json": "https://api.cartola.globo.com/patrocinadores",
    f"rodadas/{NOW}.json": "https://api.cartola.globo.com/rodadas",
    f"partidas/{NOW}.json": "https://api.cartola.globo.com/partidas",
    f"clubes/{NOW}.json": "https://api.cartola.globo.com/clubes",
    f"atletas/mercado/{NOW}.json": "https://api.cartola.globo.com/atletas/mercado",
    f"atletas/pontuados/{NOW}.json": "https://api.cartola.globo.com/atletas/pontuados",
    f"pos-rodada/destaque/{NOW}.json": "https://api.cartola.globo.com/pos-rodada/destaques",
    f"auth/time/{NOW}.json": "https://api.cartola.globo.com/auth/time",
    f"auth/time/info/{NOW}.json": "https://api.cartola.globo.com/auth/time/info",
    f"esquemas/{NOW}.json": "https://api.cartola.globo.com/esquemas",
}

VERIFY_SSL = True


def authenticate(email, password):
    """Authenticate globo.com"""
    requests.post(
        "https://login.globo.com/api/authentication",
        json=dict(
            captcha="",
            payload=dict(email=email, password=password, serviceId=4728),
        ),
        verify=VERIFY_SSL,
    )


def main(timer: func.TimerRequest) -> None:
    """Main execution"""
    logging.info("Python timer trigger function ran at %s", datetime.datetime.now())

    if helper.game_over():
        logging.info("Game is over. Do not scrape.")
        return

    logging.info("Scrape data")
    authenticate(USERNAME, PASSWORD)
    helper.scrape(CONNECTION, CONTAINER, BLOBS, HEADERS, VERIFY_SSL)
    return
