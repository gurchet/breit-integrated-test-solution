import time

from base.constants import Args
from base.services import run_tests

if __name__ == '__main__':
    print("Runner is getting started")
    time.sleep(30)
    Args.set_arguments()
    run_tests()
