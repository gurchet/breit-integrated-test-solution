import argparse
import subprocess
import sys

args = None
extra_args = None


def build_behave_command():
    behave_command = "behavex "
    for arg in extra_args:
        behave_command += arg + " "
    return behave_command


def set_arguments():
    global args
    global extra_args
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment",
                        help="Operating system of the device where you want to run the tests. i.e - platform: ["
                             "'staging','development','production']",
                        nargs='?', type=str, choices=["staging", "development", "production"], const="staging", default="staging")
    parser.add_argument("--platform",
                        help="Operating system of the device where you want to run the tests. i.e - platform: ["
                             "'ANDROID','IOS']",
                        nargs='?', type=str, choices=["ANDROID", "IOS"], const="ANDROID", default="ANDROID")
    parser.add_argument("--appium_auto_run",
                        help="Provide True if you want to auto run appium server. i.e - appium_auto_run: ['True', "
                             "'False']",
                        nargs='?', type=str, choices=["True", "False"], const="True", default="True")
    parser.add_argument("--appium_host", help="Appium url where your appium is running", nargs='?', type=str,
                        const="127.0.0.1", default="127.0.0.1")
    parser.add_argument("--app_auto_install",
                        help="Provide True if you want to auto install the AUT. i.e - app_auto_install: ['True', "
                             "'False']",
                        nargs='?', type=str, choices=["True", "False"], const="True", default="True")
    parser.add_argument("--app_path", help="The location of the AUT", type=str)
    parser.add_argument("--device_name", help="The name of devices you want to perform the test execution", type=str)
    args, extra_args = parser.parse_known_args()


def run_tests():
    cmd = build_behave_command()
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)


if __name__ == '__main__':
    set_arguments()
    run_tests()
