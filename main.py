# -*- encoding=utf8 -*-

import os
import time
import traceback
from random import choice, random
from multiprocessing import Process
from service.douyu import DouYu
from service.huya import HuYa
from chrome.driver import ChromeDriver
from utils.log import logger
from utils.error import NotUrlError, NotCookieError
from utils.redis import RedisSession
import multiprocessing

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
    with open('./words.txt', mode='r', encoding='utf8') as file:
        texts = file.read()
        texts = texts.split('\n')
        text = choice(texts)
        while True:
            chrome_obj = InitChrome()
            name = choice(platform_ls)
            platform_obj = platform_map.get(name)(chrome_obj.chrome)
            try:
                platform_obj.run(text)
            except (NotUrlError, NotCookieError) as e:
                traceback.print_exc()

                logger.error("ERROR: {}".format(e))
                time.sleep(8)
            except Exception as e:
                traceback.print_exc()

                logger.error("ERROR: {}".format(e))
                RedisSession.set_cookie(platform_obj.name + "_cookie_ls", platform_obj.cookie)
                chrome_obj.close()
                time.sleep(10)
            time.sleep(10)


def run():
    # cpu_num = os.cpu_count()
    cpu_num = 4
    logger.info("CPU NUMBER IS {}".format(cpu_num))
    process_list = []
    for _ in range(cpu_num):
        process = Process(target=init)
        process.start()
        process_list.append(process)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    run()
    input("输入任意key结束")
