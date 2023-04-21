from src.base.objects import Device
from src.utilities import capabilities_provider
from src.utilities.config_reader import get_config
from src.utilities.device_utilities import get_list_of_connected_devices


def get_available_device():
    for device_name in get_list_of_connected_devices():
        capabilities = capabilities_provider.get_capabilities(device_name)
        if capabilities is not None:
            platform = capabilities['platformName']
            if platform is get_config('platform'):
                return Device(device_name, platform, True, capabilities)
    return None
