"""Standardize procedures and have a consistent error message."""

from datetime import datetime

import requests


def get_request(url: str) -> dict:
    """Run requests.get and return the json output

    Args:
        url (str): URL for the API target

    Raises:
        HTTPError: Request failed

    Returns:
        dict: Response of the API call
    """

    response = requests.get(url=url, timeout=5)
    response.raise_for_status()

    return response.json()


def format_hour(s) -> str:
    """Convert a datetime string to hour E.g. 4 pm

    Args:
        s (string): datetime string

    Returns:
        str: Hour with units. E.g. 4 pm
    """
    return datetime.fromisoformat(s).strftime("%-I %p").lower()
