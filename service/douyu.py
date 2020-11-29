from service.base import BaseClass


class DouYu(BaseClass):
    name = "douyu"

    @property
    def is_login(self):
        if self.chrome.get_element('//div[@class="UnLogin"]'):
            return False
        super().is_login()
        return True

    def run(self, text):
        super().run(text)
        if not self.is_login:
            return

        self.chrome.send_text(xpath="//textarea[contains(@class, 'ChatSend-txt')]", text=text)
        self.chrome.click(xpath="//div[contains(@class, 'ChatSend-button')]")
