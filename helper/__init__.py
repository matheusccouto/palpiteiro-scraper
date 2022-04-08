"""Helper functions."""

from __future__ import annotations
import logging

import requests
from azure.storage.blob import ContainerClient, BlobClient


def upload_blob(connection, container, blob, body):
    """Upload blob"""
    container_client = ContainerClient.from_connection_string(connection, container)
    if not container_client.exists():
        container_client.create_container()

    blob_client = BlobClient.from_connection_string(connection, container, blob)
    blob_client.upload_blob(body)


def scrape(connection, container, blobs, headers, verify):
    """Scrape data from cartola."""
    for blob, url in blobs.items():
        logging.info("Request to %s", url)
        upload_blob(
            connection=connection,
            container=container,
            blob=blob,
            body=requests.get(url, verify=verify, headers=headers).content,
        )


def game_over(verify: bool | str = True):
    return requests.get(
        "https://api.cartola.globo.com/mercado/status",
        verify=verify,
    ).json()["game_over"]
