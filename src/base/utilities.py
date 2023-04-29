import json
import yaml
import subprocess
import socket
from contextlib import closing

from base.constants import Commands, Args, Path
from src.base.objects import Device
from ppadb.client import Client as AdbClient


def build_behave_command():
    behave_command = Commands.BEHAVEX
    for arg in Args.extra_args:
        behave_command += arg + " "
    return behave_command


def get_device():
    connected_devices = get_connected_devices()
    if len(connected_devices) < 1:
        print("No connected device found")
        return None
    available_devices = get_available_devices(connected_devices)
    if len(available_devices) < 1:
        print("No available device found")
        return None
    for device_name in available_devices:
        capabilities = get_capabilities(device_name)
        if capabilities is not None:
            platform = capabilities['platformName']
            return Device(device_name, platform, True, capabilities)
    return None


def get_available_devices(devices):
    available_devices = []
    for device_name in devices:
        if is_device_available(device_name) is True:
            available_devices.append(device_name)
    return available_devices


def is_device_available(device_name):
    return True


def get_capabilities(capability_name):
    for capability in json.load(open(get_config('capabilities_location'))):
        if capability['deviceName'] == capability_name:
            return capability
    return None


def get_config(key):
    with open(Path.CONFIG_PATH) as file:
        try:
            return search_config(yaml.load(file, yaml.FullLoader), key)
        except yaml.YAMLError as exc:
            print(exc)


def search_config(config_data, search_key):
    for key in search_key.split('.'):
        temp_config_data = config_data[key]
        if temp_config_data is None:
            print("Config {} not found".format(key))
            return None
        config_data = temp_config_data
    return config_data


def run_sync_cmd(cmd):
    return str(subprocess.run(cmd, shell=True, capture_output=True).stdout)


def run_cmd_in_spawned_process(cmd):
    subprocess.Popen(cmd, start_new_session=True, shell=True, close_fds=True)


def run_and_capture_cmd(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()


def get_connected_devices():
    host = get_config("adb_host")
    ports = get_config("adb_sockets").split(",")
    if host is None or ports is None:
        print("adb_host or adb_sockets not available")
        return None
    for port in ports:
        if not is_socket_available(host, int(port)):
            client = AdbClient(host, port)
            return client.devices()
    return None


def install_app_on_device(device_name, app_path):
    return run_sync_cmd(Commands.ADB_INSTALL.format(device_name, app_path))


def get_available_appium_socket():
    sockets = get_config("appium_sockets")
    for socket_number in sockets.split(','):
        if is_socket_available(get_config("appium_host"), int(socket_number)):
            return int(socket_number)
    return 0


def get_available_adb_socket():
    sockets = get_config("adb_sockets")
    for socket_number in sockets.split(','):
        if is_socket_available(get_config("adb_host"), int(socket_number)):
            return int(socket_number)
    return 0


def is_socket_available(host, socket_number):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, socket_number)) == 0:
            return False
        else:
            return True
