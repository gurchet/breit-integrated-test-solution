import json
import os
import socket
import subprocess
import sys
from contextlib import closing
from os.path import exists
from ppadb.device import Device

import yaml
from ppadb.client import Client as AdbClient

from base.constants import Commands, Args, Path, ROOT_PATH
from base.request_helper import get_appium_status
from base.objects import Device


def build_behave_command():
    return Commands.BEHAVE.value.format(Args.get_extra_args_str())


def get_device():
    connected_devices = get_connected_devices()
    platform = Args.get("platform")
    if connected_devices is None or len(connected_devices) < 1:
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
    for device in devices:
        if is_device_available(device.serial) is True:
            available_devices.append(device.serial)
    return available_devices


def is_device_available(device_name):
    return True


def get_capabilities(capability_name):
    for capability in json.load(open(get_capabilities_location())):
        if capability['deviceName'] == capability_name:
            return capability
    return None


def get_capabilities_location():
    location = os.path.join(ROOT_PATH, 'resources', 'capabilities.json')
    if location is not None:
        if exists(location):
            return location
    return os.path.join(ROOT_PATH, get_config('capabilities_location'))


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
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True).communicate()


def run_and_record_cmd(cmd):
    with open(get_config("logger_name"), "w") as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b""):
            sys.stdout.write(line)
            f.write(line)


def get_connected_devices():
    adb_client = get_adb_client()
    if adb_client is None:
        print("ADB client is not found")
    else:
        return adb_client.devices()


def get_adb_client():
    adb_host = Args.get("adb_host")
    if get_open_adb_service_port() is None:
        print("adb not available")
        return None
    else:
        return AdbClient(adb_host, get_open_adb_service_port())


def get_open_adb_service_port():
    adb_host = Args.get("adb_host")
    adb_ports = Args.get("adb_ports")
    adb_ports = adb_ports.split(",")
    if not (adb_ports is not None and adb_host is not None and len(adb_ports) > 0):
        print("No sockets or host found to check open port")
        return 0
    for adb_port in adb_ports:
        if not is_port_available(adb_host, int(adb_port)):
            return int(adb_port)
    return 0


def get_open_appium_service_port():
    for port in Args.get("appium_port").split(","):
        if is_appium_running_on_port(port):
            return port
    return 0


def is_appium_running_on_port(port):
    response = get_appium_status(port)
    if response is not None and response.status_code == 200:
        return True
    else:
        False


def install_app_on_device(device_name, app_path):
    return run_sync_cmd(Commands.ADB_INSTALL.value.format(device_name, app_path))


def get_available_appium_service_port():
    ports = Args.get("appium_ports").split(",")
    host = Args.get("appium_host")
    for port in ports:
        port = int(port)
        if is_port_available(host, int(port)):
            return int(port)
    return 0


def is_port_available(host, port_number):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port_number)) == 0:
            return False
        else:
            return True
