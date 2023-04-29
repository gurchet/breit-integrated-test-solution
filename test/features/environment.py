from base.services import quit_driver, stop_appium_service


def before_all(context):
    print('Before all executed')


def before_scenario(scenario, context):
    print('Before scenario executed')


def after_scenario(scenario, context):
    quit_driver()


def after_all(context):
    stop_appium_service()
