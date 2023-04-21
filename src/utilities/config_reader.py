import yaml


def get_config(key):
    with open('config.yaml') as file:
        try:
            search(yaml.safe_load(file), key)
        except yaml.YAMLError as exc:
            print(exc)


def search(config_data, search_key):
    for key in search_key.split('.'):
        config_data = config_data[key]
    return config_data
