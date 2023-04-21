import os
import subprocess


def run_cmd(cmd):
    os.system(cmd)


def run_and_capture_cmd(cmd):
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out
