import argparse
import os
from enum import Enum

ROOT_PATH = os.path.dirname(os.path.abspath('__file__'))[0:-8]


class DevicePlatform(Enum):
    ANDROID = "android"
    IOS = "ios"


class Commands(Enum):
    ADB_DEVICES = "source ~/.bash_profile;adb devices"
    ADB_INSTALL = "source ~/.bash_profile;adb -s {} install -r {}"
    BEHAVEX = "source ~/.bash_profile;behavex "
    APPIUM = "source ~/.bash_profile;appium -p {}"
    APP_KILL = "source ~/.bash_profile;kill -9 {}"
    ADB_START = "source ~/.bash_profile;adb -P {} start-server"
    ADB_STOP = "source ~/.bash_profile;adb kill-server"


class Urls(Enum):
    APPIUM_HUB_URL = "http://{}:{}/wd/hub"
    APPIUM_STATUS_URL = "http://{}:{}/wd/hub/status"


class Path:
    CONFIG_PATH = os.path.join(ROOT_PATH, 'config.yaml')


class Args:
    main_args = None
    extra_args = None

    @classmethod
    def get_main_args(cls):
        return cls.main_args

    @classmethod
    def get_extra_args(cls):
        return cls.main_args

    @classmethod
    def get(cls, name):
        return cls.main_args[name] if name in cls.main_args is not None else cls.extra_args[name]

    @classmethod
    def convert_extra_args_to_dict(cls, extra_args_list):
        args_str = ''
        converted_dict = {}
        for extra_arg in extra_args_list:
            args_str += extra_arg + " "
        args_str_list = args_str.strip().split("--")
        for processed_args_str in args_str_list:
            processed_args_str = processed_args_str.strip()
            item = None
            if len(processed_args_str) < 1:
                continue
            if ' ' in processed_args_str:
                item = processed_args_str.split(' ')
            elif '=' in processed_args_str:
                item = processed_args_str.split('=')
            if item is None:
                continue
            if len(item) == 1:
                converted_dict[str(item.strip())] = ''
            elif len(item) == 2:
                converted_dict[str(item[0]).strip()] = str(item[1]).strip()
            elif len(item) > 2:
                converted_dict[str(item[0]).strip()] = item[1:]
            else:
                continue
        return converted_dict

    @classmethod
    def set_arguments(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--environment",
                            help="Operating system of the device where you want to run the tests. i.e - platform: ["
                                 "'staging','development','production']",
                            nargs='?', type=str, choices=["staging", "development", "production"], const="staging",
                            default="staging")
        parser.add_argument("--platform",
                            help="Operating system of the device where you want to run the tests. i.e - platform: ["
                                 "'ANDROID','IOS']",
                            nargs='?', type=str, choices=["ANDROID", "IOS"], const="ANDROID", default="ANDROID")
        parser.add_argument("--appium_auto_run",
                            help="Provide True if you want to auto run appium server. i.e - appium_auto_run: ['True', "
                                 "'False']",
                            nargs='?', type=str, choices=["True", "False"], const="True", default="True")
        parser.add_argument("--appium_host", help="Appium host where your appium is running. i.e 127.0.0.1",
                            nargs='?',
                            type=str,
                            const="127.0.0.1", default="127.0.0.1")
        parser.add_argument("--appium_port", help="Appium port where your appium is running. i.e 4723",
                            nargs='?',
                            type=str,
                            const="4723", default="4723")
        parser.add_argument("--app_auto_install",
                            help="Provide True if you want to auto install the AUT. i.e - app_auto_install: ['True', "
                                 "'False']",
                            nargs='?', type=str, choices=["True", "False"], const="True", default="True")
        parser.add_argument("--app_path", help="The location of the AUT", type=str)
        args, extra_args = parser.parse_known_args()
        cls.main_args = vars(args)
        cls.extra_args = cls.convert_extra_args_to_dict(extra_args)
