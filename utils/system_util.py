import sys
from os.path import dirname, join, abspath


def is_windows():
    return sys.platform in ('win32', 'cygwin')


def is_linux():
    return sys.platform.startswith('linux')


def get_canonical_os_name():
    if is_windows():
        return 'windows'
    elif is_linux():
        return 'linux'


def locate_web_driver():
    driver_name = "chromedriver"
    if is_windows():
        driver_name = 'chromedriver.exe'
    return join(dirname(dirname(abspath(__file__))), "chrome", get_canonical_os_name(), driver_name)
