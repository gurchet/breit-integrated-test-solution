import json
import yaml
import subprocess
import socket
from contextlib import closing

from base.constants import Commands, Args, Path
from src.base.objects import Device


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
        config_data = config_data[key]
    return config_data


def run_sync_cmd(cmd):
    return str(subprocess.run(cmd, shell=True, capture_output=True).stdout)


def run_cmd_in_spawned_process(cmd):
    subprocess.Popen(cmd, start_new_session=True, shell=True, close_fds=True)


def run_and_capture_cmd(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()


def get_connected_devices():
    connected_devices = []
    devices_str = run_sync_cmd(Commands.ADB_DEVICES)
    devices_str = devices_str[31:]
    if len(devices_str) < 3:
        return []
    for device in devices_str.split(' '):
        connected_devices.append(device)
    return connected_devices


def install_app_on_device(device_name, app_path):
    return run_sync_cmd(Commands.ADB_INSTALL.format(device_name, app_path))


def get_available_socket():
    sockets = get_config("sockets")
    for socket_number in sockets.split(','):
        if is_port_available(get_config("appium_host"), int(socket_number)):
            return int(socket_number)
    return 0


def is_port_available(host="127.0.0.1", socket_number=8080):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, socket_number)) == 0:
            return False
        else:
            return True
