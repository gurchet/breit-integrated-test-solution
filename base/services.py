import sys
import time
from urllib.parse import urlparse

from appium import webdriver

from base.constants import Commands, Args, Urls, CurrentRun
from base.utilities import install_app_on_device, get_device, build_behave_command, \
    run_and_capture_cmd, run_cmd_in_spawned_process, run_sync_cmd, \
    get_open_adb_service_port, get_available_appium_service_port, is_appium_running_on_port, get_config, \
    get_capabilities_location


def run_tests():
    output, error = run_and_capture_cmd(build_behave_command())
    if output is not None:
        print(output)
    if error is not None:
        print(error)


def get_driver():
    return CurrentRun.current_driver


def perform_complete_set_up():
    if setup_adb() is False:
        return False
    if setup_device() is False:
        return False
    if setup_appium() is False:
        return False
    if setup_driver() is False:
        return False


def setup_driver():
    if CurrentRun.current_driver is None:
        CurrentRun.current_driver = webdriver.Remote(CurrentRun.current_appium,
                                                     CurrentRun.current_device.get_capabilities())
        if CurrentRun.current_driver is not None:
            print("The driver created successfully")
            return True
        else:
            print("The driver could not get created")
            return False
    else:
        print("The driver already exists")
        return True


def setup_appium():
    if Args.get('appium_auto_run') == 'False':
        CurrentRun.current_appium = urlparse(
            Urls.APPIUM_HUB_URL.value.format(Args.get("appium_host"), Args.get("appium_port")))
        return True
    if CurrentRun.current_appium is None:
        port_number = get_available_appium_service_port()
        if port_number == 0:
            print("Could not get the free port for appium")
            return False
        else:
            start_appium_service(port_number)
            CurrentRun.current_appium = urlparse(
            Urls.APPIUM_HUB_URL.value.format(Args.get("appium_host"), port_number))
            return True
    else:
        if is_appium_running_on_port(CurrentRun.current_appium.port):
            print("Appium server is already started on port {}!".format(CurrentRun.current_appium.port))
        else:
            if start_appium_service(CurrentRun.current_appium.port):
                CurrentRun.current_appium = urlparse(
                    Urls.APPIUM_HUB_URL.value.format(Args.get("appium_host"), CurrentRun.current_appium.port))
                return True
            else:
                return False


def setup_device():
    if CurrentRun.current_device is None:
        CurrentRun.current_device = get_device()
        if CurrentRun.current_device is None:
            print("Device could get created")
            return False
        else:
            print("Device created successfully!")
    else:
        print("Device already exists")
    if Args.get('app_path') is not None:
        result = install_app_on_device(CurrentRun.current_device.get_name(), Args.get('app_path'))
        if "Success" in result:
            print("App is installed successfully!")
            return True
        else:
            print("The app could not get installed in device " + CurrentRun.current_device.get_name())
            return False
    else:
        print("App path is missing in args")


def setup_adb():
    if not is_adb_service_running():
        return start_adb_service()
    else:
        print("adb service is already running!")
        return True


def start_appium_service(port):
    try:
        run_cmd_in_spawned_process(Commands.APPIUM.value.format(port))
        print("appium service is started successfully!")
        return True
    except Exception:
        return False


def start_adb_service():
    try:
        run_cmd_in_spawned_process(Commands.ADB_START.value.format(Args.get("adb_port").split(",")[0]))
        print("adb service is started")
        return True
    except Exception:
        return False


def stop_adb():
    run_sync_cmd(Commands.ADB_STOP.value)
    print("adb service stopped")


def is_adb_service_running():
    if get_open_adb_service_port() == 0:
        return False
    else:
        return True


def stop_appium():
    appium_auto_run = Args.get("appium_auto_run")
    if appium_auto_run is None or appium_auto_run == "True":
        print("Stopping Appium server")
        run_sync_cmd(Commands.APP_KILL.value.format(CurrentRun.current_appium.port))
        CurrentRun.current_appium = None
    else:
        print("Appium service was not started hence not required to stop")


def quit_driver():
    if CurrentRun.current_driver is not None:
        CurrentRun.current_driver.quit()
        CurrentRun.current_driver = None


if __name__ == '__main__':
    Args.set_arguments()
    setup_adb()
    setup_device()
    setup_appium()
    setup_driver()
    quit_driver()
    stop_appium()
    stop_adb()
