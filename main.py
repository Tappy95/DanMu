# -*- encoding=utf8 -*-

import time
import traceback
from service.huya import HuYa
from os import cpu_count
from random import choice
from multiprocessing import Process
from service.douyu import DouYu
from chrome.driver import ChromeDriver
from utils.log import logger
from utils.error import NotUrlError, NotCookieError
from utils.redis import RedisSession
import multiprocessing

platform_map = {
    # "douyu": DouYu,
    "huya": HuYa
}

platform_ls = [key for key in platform_map.keys()]
chrome_obj = None

def get_words():
    with open('words.txt', 'r', encoding='utf-8') as f:
        return f.read().split('\n')


class InitChrome:
    _instance = None
    _chrome = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._chrome = ChromeDriver()
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


def init(text_ls):
    global chrome_obj
    while True:
        chrome_obj = InitChrome()
        name = choice(platform_ls)
        platform_obj = platform_map.get(name)(chrome_obj.chrome)
        try:
            platform_obj.run(choice(text_ls))
        except (NotUrlError, NotCookieError) as e:
            logger.error("ERROR: {}".format(e))
            time.sleep(8)
        except Exception as e:
            traceback.print_exc()
            logger.error("ERROR: {}".format(e))
            if not platform_obj.cookie_set: RedisSession.set_cookie(platform_obj.name + "_cookie_ls", platform_obj.cookie)
            chrome_obj.close()
            time.sleep(3)
        else:
            time.sleep(3)


def run(c):
    logger.info("CPU NUMBER IS {}".format(c))
    process_list = []
    text_ls = get_words()
    for _ in range(c):
        process = Process(target=init, args=(text_ls,))
        process.start()
        process_list.append(process)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cpu_num = cpu_count()
    while True:
        c_count = input('请输入浏览器个数:')
        if c_count.isdigit():
            c = int(c_count) if int(c_count) <= cpu_num else cpu_num
            run(c)
            break
        else:
            print("请输入数字")
    input("输入任意key结束")
