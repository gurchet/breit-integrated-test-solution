from base.services import quit_driver, stop_appium_service, setup_adb, setup_device, setup_appium, setup_driver, \
    stop_adb_service


def before_all(context):
    print('Before all executed')
    setup_adb()


def before_scenario(scenario, context):
    print('Before scenario executed')
    setup_device()
    setup_appium()
    setup_driver()


def after_scenario(scenario, context):
    quit_driver()
    stop_appium_service()
    quit_driver()

def after_all(context):
    stop_adb_service()
