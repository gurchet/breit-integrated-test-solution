from src.utilities.command_runner import run_and_capture_cmd, run_cmd


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
