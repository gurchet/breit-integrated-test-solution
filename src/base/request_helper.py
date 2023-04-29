import requests as requests
from requests.exceptions import ConnectionError


def get_appium_status(url):
    try:
        return requests.get(url, timeout=0.001)
    except ConnectionError as e:
        return None

