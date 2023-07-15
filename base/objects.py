from base.loggings import Logging

logger = Logging.get_logger(__name__)


class Device:

    def __init__(self, name, os, availability, capabilities):
        self.__name = name
        self.__os = os
        self.__availability = availability
        self.__capabilities = capabilities

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_os(self):
        return self.__os

    def set_os(self, os):
        self.__os = os

    def get_availability(self):
        return self.__availability

    def set_availability(self, availability):
        self.__availability = availability

    def get_capabilities(self):
        return self.__capabilities

    def set_capabilities(self, capabilities):
        self.__capabilities = capabilities
