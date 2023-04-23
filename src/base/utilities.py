import json
import yaml
import os
import subprocess
import socket
from contextlib import closing
from src.base.objects import Device


def get_available_device():
    for device_name in get_list_of_connected_devices():
        capabilities = get_capabilities(device_name)
        if capabilities is not None:
            platform = capabilities['platformName']
            if platform is get_config('platform'):
                return Device(device_name, platform, True, capabilities)
    return None


def get_capabilities(capability_name):
    for capability in json.load(open(get_config('capabilities_location'))):
        if capability['deviceName'] == capability_name:
            return capability


def get_config(key):
    with open('config.yaml') as file:
        try:
            return search_config(yaml.safe_load(file), key)
        except yaml.YAMLError as exc:
            print(exc)


def search_config(config_data, search_key):
    for key in search_key.split('.'):
        config_data = config_data[key]
    return config_data


def run_cmd(cmd):
    os.system(cmd)


def run_and_capture_cmd(cmd):
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out


def get_list_of_connected_devices():
    connected_devices = []
    devices = run_and_capture_cmd("source ~/.bash_profile;adb devices")
    devices = devices.replace("List of devices attached", "")
    devices = devices.replace("device", "")
    for device in devices.split(' '):
        connected_devices.append(device)
    return connected_devices


def install_app_on_device(device_name, app_path):
    run_cmd("source ~/.bash_profile;adb -s " + device_name + " install -r " + app_path)


def get_available_socket():
    sockets_list = get_config("sockets").split(",")
    for socket_number in sockets_list:
        if is_port_available(get_config("appium_host"), socket_number):
            return int(socket_number)
    return 0


def is_port_available(host="127.0.0.1", socket_number=8080):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, socket_number)) == 0:
            return True
        else:
            return False
