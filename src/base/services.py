from base.constants import Commands, Args, Urls
from base.request_helper import get_appium_status
from src.base.utilities import install_app_on_device, get_device, build_behave_command, \
    get_config, run_and_capture_cmd, run_cmd_in_spawned_process, run_sync_cmd, get_available_appium_socket, is_socket_available
from urllib.parse import urlparse
from appium import webdriver

current_device = None
current_appium = None
current_driver = None


def run_tests():
    run_and_capture_cmd(build_behave_command())


def get_driver():
    perform_complete_set_up()
    return current_driver


def perform_complete_set_up():
    global current_appium
    if setup_adb() is False:
        return False
    if setup_device() is False:
        return False
    if setup_appium() is False:
        return False
    if setup_driver() is False:
        return False


def setup_driver():
    global current_driver
    if current_driver is None:
        current_driver = webdriver.Remote(current_appium, current_device.get_capabilities())
        if current_driver is not None:
            print("The driver created successfully")
            return True
        else:
            print("The driver could not get created")
            return False
    else:
        print("The driver already exists")
        return True


def setup_appium():
    global current_appium
    if Args.get('appium_auto_run') == 'False':
        current_appium = urlparse(
            Urls.APPIUM_HUB_URL.value.format(get_config("appium_host"), get_config("appium_port")))
        return True
    if current_appium is None:
        if start_appium_service() is False:
            print("Appium server could not started successfully")
            return False
        else:
            print("Appium server running")
            return True
    else:
        print("Appium server is already started")
        return True


def setup_device():
    global current_device
    if current_device is None:
        current_device = get_device()
        if current_device is None:
            print("Could not fetch available device")
            return False
    else:
        print("Device already exists")
    if install_app_on_device(current_device.get_name(), Args.get('app_path')) != 0:
        print("The app could not get installed in device " + current_device.get_name())
        return False
    return True


def setup_adb():
    if not is_adb_service_running():
        return start_adb_service()
    else:
        print("adb service is already running")
        return True


def start_appium_service():
    global current_appium
    socket_number = get_available_appium_socket()
    if socket_number == 0:
        print("Could not get the free port")
        return
    temp_appium_url = Urls.APPIUM_HUB_URL.value.format(get_config("appium_host"), socket_number)
    if is_appium_service_running(temp_appium_url) is True:
        print("Appium service already running")
        return True
    run_cmd_in_spawned_process(Commands.APPIUM.value.format(socket_number))
    current_appium = urlparse(temp_appium_url)


def start_adb_service():
    if get_config("adb_sockets") is not None and get_config("adb_sockets")[0] is not None:
        run_cmd_in_spawned_process(Commands.ADB_START.value.format(get_config("adb_sockets").split(",")[0]))
        print("adb service is started")
    else:
        print("No socket provided in the config.yaml")
        return False


def stop_adb_service():
    run_sync_cmd(Commands.ADB_STOP.value)
    print("adb service stopped")


def get_open_adb_service_port():
    adb_sockets = get_config("adb_sockets").split(",")
    adb_host = get_config("adb_host")
    if not (adb_sockets is not None and adb_host is not None and len(adb_sockets) > 0):
        print("No sockets or host found in config.yaml to check open port")
        return 0
    for adb_socket in adb_sockets:
        if not is_socket_available(get_config("adb_host"), int(adb_socket)):
            return int(adb_socket)
    return 0


def is_adb_service_running():
    if get_open_adb_service_port() == 0:
        return False
    else:
        return True


def is_appium_service_running(appium_url):
    response = get_appium_status(appium_url + "/status")
    if response is not None and response.status_code == 200:
        return True
    else:
        False


def stop_appium_service():
    global current_appium
    appium_auto_run = Args.get("appium_auto_run")
    if appium_auto_run is None or appium_auto_run == "True":
        print("Stopping Appium server")
        run_sync_cmd(Commands.APP_KILL.value.format(current_appium.port))
        current_appium = None
    else:
        print("Appium service was not started hence not required to stop")


def quit_driver():
    global current_driver
    if current_driver is not None:
        current_driver.quit()
        current_driver = None


if __name__ == '__main__':
    Args.set_arguments()
    setup_adb()
    stop_adb_service()
