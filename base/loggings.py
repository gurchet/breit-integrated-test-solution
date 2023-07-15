import logging

logging.getLogger("breit_Logging").setLevel(logging.CRITICAL)


class Logging:
    PACKAGE_NAME = "base"
    DEFAULT_FORMAT = logging.Formatter(
        fmt='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S')
    DEFAULT_LEVEL = logging.CRITICAL

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        if logger.handlers:
            logger.handlers[0].setFormatter(cls.DEFAULT_FORMAT)
        return logger

    @classmethod
    def set_default_format(cls, format):
        cls.DEFAULT_FORMAT = format

    @classmethod
    def disable(cls):
        logging.getLogger(cls.PACKAGE_NAME).setLevel(logging.CRITICAL)

    @classmethod
    def enable(cls, level=logging.DEBUG):
        logging.getLogger(cls.PACKAGE_NAME).setLevel(level)
