import sys

from base.constants import Args
from base.loggings import Logging
from base.services import setup_adb, setup_appium, setup_device, setup_driver, quit_driver, stop_appium, \
    stop_adb, perform_complete_set_up

logger = Logging.get_logger(__name__)


def before_all(context):
    logger.info('Before all executed')
    Args.set_arguments()
    if setup_adb() is False:
        sys.exit("adb service could not get started")
    if setup_device() is False:
        sys.exit("The device could not get setup")
    if setup_appium() is False:
        sys.exit("The appium service could not get started")


def before_scenario(scenario, context):
    logger.info('Before scenario executed')
    setup_driver()


def after_scenario(scenario, context):
    logger.info('After scenario executed')
    quit_driver()


def after_all(context):
    logger.info('After all executed')
    stop_appium()
    stop_adb()
