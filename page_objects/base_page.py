import logging

from base.services import get_driver

LOGGER = logging.getLogger(__name__)


class BasePage(object):
    def __init__(self, explicit_wait=30):
        self._driver = get_driver()
        self._explicit_wait = explicit_wait

    def click(self, locator):
        self._driver.find_element(locator).click()
