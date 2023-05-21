import logging

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage

LOGGER = logging.getLogger(__name__)


class LoginPage(BasePage):
    def click_on_login_button(self):
        self.click(By.id(''))
