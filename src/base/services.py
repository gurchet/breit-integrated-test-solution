import threading

from src.base import utilities
from src.base.utilities import get_config, get_available_device
from urllib.parse import urlparse
from appium import webdriver

socket_number = 0
drivers = {}


def get_appium_driver():
    desired_key = threading.get_ident()

    for current_key, current_driver in drivers.items():
        if desired_key == current_key:
            return current_driver["driver"]
    device = get_available_device()
    if device is None:
        print("No connected device found")
        return None
    capabilities = device.get_capabilities()
    if capabilities is None:
        print("No capabilities found for the device " + device.get_name())
        return None

    driver = webdriver.Remote(get_appium_server_url(), capabilities);
    map_driver_device = {"device": device, "driver": driver}
    drivers[threading.get_ident()] = map_driver_device
    return driver


def quit_current_driver():
    desired_key = threading.get_ident()
    get_appium_driver().quit()
    drivers.remove(desired_key)


def start_appium_service():
    global socket_number
    if get_config("appium_auto_run") == "false":
        socket_number = int(get_config("ports").split(",")[0])
        print("Appium service is not getting started as flag appium_auto_run is false. To run appium service in auto "
              "mode, please turn the flag appium_auto_run to true")
        return
    print("Starting Appium server")
    socket_number = utilities.get_available_socket()
    utilities.run_cmd("appium -p " + socket_number)


def stop_appium_service():
    if get_config("appium_auto_run") == "false":
        print("Appium service was not started hence not required to stop")
        return
    print("Stopping Appium server")
    utilities.run_cmd("kill -9 " + socket_number)


def get_appium_server_url():
    urlparse("http://" + get_config("appium_host_url") + ":" + socket_number + "/wd/hub/")
