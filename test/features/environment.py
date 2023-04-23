def before_all(context):
    print('Before all executed')


def before_scenario(scenario, context):
    print('Before scenario executed')


def after_feature(scenario, context):
    print('After feature executed')


def after_all(context):
    print('After all executed')
