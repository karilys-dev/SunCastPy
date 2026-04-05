"""Standardize procedures and have a consistent error message."""

from datetime import datetime

import requests


def get_request(url: str) -> dict:  # pragma: no cover
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
    """Format datetime to hour E.g. 4:00 pm

    Args:
        hour (string | datetime): datetime string

    Returns:
        str: Hour with units.
    """
    if isinstance(hour, str):
        hour = datetime.fromisoformat(hour)
    return hour.strftime("%-I:%M %p").lower()


def format_date(date: str | datetime, dayname=True) -> str:
    """Format datetime %A %Y-%m-%d. E.g. Monday YYYY-MM-DD

    Args:
        date (string): datetime string

    Returns:
        str: Formatted date %A %Y-%m-%d
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    if dayname:
        return date.strftime("%A %Y-%m-%d")
    else:
        return date.strftime("%Y-%m-%d")
