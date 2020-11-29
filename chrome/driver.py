# -*- encoding=utf8 -*-

import time
import json
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from helium import *

Config.implicit_wait_secs = 25

with open('stealth.min.js') as f:
    js = f.read()


class ChromeDriver:
    def __init__(self, headless=False):
        options = ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--incognito')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-logging")
        options.add_argument('--log-level=2')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')  # 无头浏览器
        self.driver = start_chrome(url="https://www.baidu.com", headless=headless, options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def get_web(self, url, second=10):
        go_to(url)
        time.sleep(second)

    def send_text(self, xpath, text="", second=1):
        write(text, S(xpath))
        time.sleep(second)

    def click_button(self, xpath):
        click(S(xpath))

    def click_js(self, xpath):
        self.execute_script("arguments[0].click()", self.get_element(xpath))

    def click(self, xpath, second=1):
        try:
            self.click_js(xpath)
        except:
            self.click_button(xpath)
        time.sleep(second)

    def set_cookie(self, url, cookie):
        domain = urlparse(url).netloc.replace("www.", "")
        if isinstance(cookie, str):
            try:
                cookie = json.loads(cookie)
            except:
                cookie = {c.split("=", 1)[0]: c.split("=", 1)[1] for c in cookie.split("; ")}
        cookies = [
            {"name": key, "value": value, "path": "/", "domain": ".{}".format(domain)} for key, value in cookie.items()
        ]
        self.driver.delete_all_cookies()
        time.sleep(0.5)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        time.sleep(0.5)

    def wait_element(self, xpath):
        try:
            WebDriverWait(self.driver, 25, 0.01).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except:
            return False

    def execute_script(self, script, cla=None, second=0):
        self.driver.execute_script(script, cla) if cla else self.driver.execute_script(script)
        time.sleep(second)

    def get_element(self, xpath):
        last_time = int(time.time()) + 3
        while int(time.time()) < last_time:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements: return elements[0]
