import json

from src.utilities.config_reader import get_config


def get_capabilities(capability_name):
    for capability in json.load(open(get_config('capabilities_location'))):
        if capability['deviceName'] == capability_name:
            return capability
