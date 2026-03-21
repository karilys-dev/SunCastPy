"""Standardize procedures and have a consistent error message."""

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

    response = requests.get(url=url)
    response.raise_for_status()

    return response.json()
