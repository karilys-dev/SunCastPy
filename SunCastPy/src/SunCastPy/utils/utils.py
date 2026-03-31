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


def format_hour(hour: str | datetime) -> str:
    """Convert a datetime string to hour E.g. 4 pm

    Args:
        hour (string): datetime string

    Returns:
        str: Hour with units. E.g. 4 pm
    """
    if isinstance(hour, str):
        hour = datetime.fromisoformat(hour)
    return hour.strftime("%-I %p").lower()


def format_date(date: str | datetime) -> str:
    """Convert a datetime string to hour E.g. 4 pm

    Args:
        date (string): datetime string

    Returns:
        str: Formatted date %A %Y-%m-%d. E.g. Monday 2026-12-31
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return date.strftime("%A %Y-%m-%d")
