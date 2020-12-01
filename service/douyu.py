from service.base import BaseClass


class DouYu(BaseClass):
    name = "douyu"

    def is_login(self):
        self.chrome.get_web("https://www.douyu.com/member", second=0)
        if self.chrome.get_element('//div[@id="loginbox-con"]', second=0):
            return False
        super().is_login()
        return True

    def run(self, text):
        super().run(text)
        if not self.is_login():
            return

        self.chrome.get_web(self.url, second=2)
        self.chrome.send_text(xpath="//textarea[contains(@class, 'ChatSend-txt')]", text=text, second=1)
        self.chrome.click(xpath="//div[contains(@class, 'ChatSend-button')]", second=1)
