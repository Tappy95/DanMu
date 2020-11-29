from service.base import BaseClass


class HuYa(BaseClass):
    name = "huya"

    @property
    def is_login(self):
        if not self.chrome.get_element('//div[contains(@class, "success-login")]').get_attribute("style"):
            return False
        super().is_login()
        return True

    def run(self, text):
        super().run(text)
        if not self.is_login:
            return

        self.chrome.send_text(xpath="//textarea[contains(@id, 'pub_msg_input')]", text='666,牛逼铁子:麒麟趣玩在家赚钱')
        self.chrome.click(xpath="//span[contains(@id, 'msg_send_bt')]")
