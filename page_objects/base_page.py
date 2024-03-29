import logging

from base.services import get_driver

LOGGER = logging.getLogger(__name__)


class BasePage(object):
    def __init__(self, explicit_wait=30):
        self.driver = get_driver()
        self._explicit_wait = explicit_wait

    def click(self, locator):
        self.driver.find_element(locator).click()
