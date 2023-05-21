import requests as requests
from requests.exceptions import ConnectionError

from base.constants import Args, Urls


def get_appium_status(port):
    try:
        return requests.get(Urls.APPIUM_STATUS_URL.value.format(Args.get("appium_host"), port))
    except ConnectionError as e:
        return None

