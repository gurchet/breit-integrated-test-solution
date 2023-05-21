from behave import *
from page_objects.adr.Login import LoginPage


@given("user logs into the app")
def step_payment(context):
    LoginPage().click_on_login_button()
