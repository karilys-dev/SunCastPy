import requests


def get_request(url: str) -> dict:
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Request failed with status code: {response.status_code}")
