import argparse
import os
from enum import Enum

from base.loggings import Logging

ROOT_PATH = os.path.dirname(os.path.abspath('__file__')).removesuffix('/base')
logger = Logging.get_logger(__name__)


class CurrentRun(object):
    current_device = None
    current_appium = None
    current_driver = None


class DevicePlatform(Enum):
    ANDROID = "android"
    IOS = "ios"


class Commands(Enum):
    ADB_DEVICES = "source ~/.bash_profile;adb devices"
    ADB_INSTALL = "source ~/.bash_profile;adb -s {} install -r {}"
    BEHAVEX = "source ~/.bash_profile;behavex {}"
    BEHAVE = "source ~/.bash_profile;behave {}"
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
    def get_extra_args_str(cls):
        return " ".join(cls.extra_args)

    @classmethod
    def get_extra_args_dict(cls):
        return cls.convert_extra_args_to_dict(cls.extra_args)

    @classmethod
    def get(cls, name):
        return cls.get_main_args()[name] if name in cls.get_main_args() is not None else cls.get_extra_args_dict()[name]

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
                                 "'android','ios']",
                            nargs='?', type=str, choices=["android", "ios"], default="android")
        parser.add_argument("--appium_auto_run",
                            help="Provide True if you want to auto run appium server. i.e - appium_auto_run: ['True', "
                                 "'False']",
                            nargs='?', type=str, choices=["True", "False"], const="True", default="True")
        parser.add_argument("--appium_host", help="Appium host where your appium is running. i.e 127.0.0.1",
                            nargs='?',
                            type=str,
                            const="127.0.0.1", default="127.0.0.1")
        parser.add_argument("--adb_host", help="ADB host where your appium is running. i.e 127.0.0.1",
                            nargs='?',
                            type=str,
                            const="127.0.0.1", default="127.0.0.1")
        parser.add_argument("--appium_ports", help="Appium port where your appium is running. i.e 4723",
                            nargs='?',
                            type=str,
                            const="4723", default="4723")
        parser.add_argument("--adb_ports", help="ADB port where your adb is running. i.e 5037",
                            nargs='?',
                            type=str,
                            const="5037", default="5037")
        parser.add_argument("--app_auto_install",
                            help="Provide True if you want to auto install the AUT. i.e - app_auto_install: ['True', "
                                 "'False']",
                            nargs='?', type=str, choices=["True", "False"], const="True", default="True")
        parser.add_argument("--app_path", help="The location of the AUT", nargs='?', type=str, const="~/Downloads"
                                                                                                     "/aut.apk",
                            default="~/Downloads/aut.apk")
        args, extra_args = parser.parse_known_args()
        cls.main_args = vars(args)
        cls.extra_args = extra_args
