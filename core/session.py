import string

from playwright.async_api import ProxySettings
from data.config import HEADLESS, BROWSER_TYPE, SESSION_DATA_DIR
from playwright.sync_api import sync_playwright
from random import randint, choices


class Session:
    def __init__(self, headless: bool = HEADLESS, browser_type: str = BROWSER_TYPE, proxy: ProxySettings = None):
        self.headless = headless
        self.browser_type = browser_type
        self.playwright = None
        self.browser = None
        self.context = None
        self.current_page = None
        self.mouse_position = None
        self.proxy = proxy
        self.pages = []


    def start(self):
        self.playwright = sync_playwright().start()
        user_data_dir = SESSION_DATA_DIR + ''.join(choices(string.ascii_letters + string.digits, k=8)).lower()

        if self.browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=self.headless, proxy=self.proxy)
        elif self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=self.headless, proxy=self.proxy)
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=self.headless, proxy=self.proxy)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser}")

        self.context = self.browser.new_context()
        self.current_page = self.context.new_page()
        self.pages.append(self.current_page)
        self.mouse_position = self._get_first_mouse_position()

        return self.current_page

    def stop(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def create_page(self):
        self.current_page = self.context.new_page()
        self.pages.append(self.current_page)

        return self.current_page

    def set_current_page(self, page):
        self.current_page = page
        self.current_page.focus()

    def _get_first_mouse_position(self):
        viewport = self.current_page.viewport_size
        start_x = randint(0, viewport["width"])
        start_y = randint(0, viewport["height"])

        return {"x": start_x, "y": start_y}

    def set_mouse_position(self, x, y):
        self.mouse_position = {"x": x, "y": y}
