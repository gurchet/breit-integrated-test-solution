import time

from base.constants import Args
from base.loggings import Logging
from base.services import run_tests

logger = Logging.get_logger(__name__)


if __name__ == '__main__':
    logger.info("Runner is getting started")
    time.sleep(30)
    Args.set_arguments()
    run_tests()
