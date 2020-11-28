# -*- encoding=utf8 -*-

import os
import time
from random import choice
from multiprocessing import Process
from service.douyu import DouYu
from service.huya import HuYa
from chrome.driver import ChromeDriver
from utils.log import logger
from utils.error import NotUrlError, NotCookieError
from utils.redis import RedisSession

platform_map = {
    "douyu": DouYu,
    "huya": HuYa
}

platform_ls = [key for key in platform_map.keys()]


class InitChrome:
    _instance = None
    _chrome = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._chrome = ChromeDriver(headless=False)
        return cls._instance

    @property
    def chrome(self):
        return self._chrome

    @classmethod
    def close(cls):
        if cls._chrome: cls._chrome.close()
        cls._chrome = None
        cls._instance = None

    def __del__(self):
        if self._chrome: self._chrome.close()


def init():
    while True:
        chrome_obj = InitChrome()
        name = choice(platform_ls)
        platform_obj = platform_map.get(name)(chrome_obj.chrome)
        try:
            platform_obj.run()
        except (NotUrlError, NotCookieError) as e:
            logger.error("ERROR: {}".format(e))
            time.sleep(8)
        except Exception as e:
            logger.error("ERROR: {}".format(e))
            RedisSession.set_cookie(platform_obj.name + "_cookie_ls", platform_obj.cookie)
            chrome_obj.close()
            time.sleep(10)
        time.sleep(10)


def run():
    cpu_num = os.cpu_count()
    logger.info("CPU NUMBER IS {}".format(cpu_num))
    process_list = []
    for _ in range(cpu_num):
        process = Process(target=init)
        process.start()
        process_list.append(process)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    run()
