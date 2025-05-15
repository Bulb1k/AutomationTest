import time

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from core.session import Session
from data.config import TIMEOUT, DELAYS
from random import randint, uniform


class BasePage:
    def __init__(self, session: Session):
        self.page: Page = session.current_page
        self.mouse_position = session.mouse_position

    def go_to(self, url: str):
        self.page.goto(url)

    def click(self, selector: str, timeout: int = TIMEOUT, delay: list = DELAYS['click']):
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector, delay=randint(*delay))
        except PlaywrightTimeoutError:
            raise Exception(f"Element with selector '{selector}' not found for clicking.")\


    def click_by_human(self, selector: str, timeout: int = TIMEOUT, delay: list = DELAYS['click']):
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)

            box = element.bounding_box()
            if not box:
                raise Exception(f"Cannot determine bounding box for selector '{selector}'.")

            if not self.is_element_in_viewport(box):
                self.scroll_to_element_like_human(box)
                box = element.bounding_box()

            end_position = {
                "x": box['x'] + box['width'] / 2,
                "y": box['y'] + box['height'] / 2
            }

            self.human_like_mouse_move(self.mouse_position, end_position)
            self.page.mouse.click(x=end_position["x"], y=end_position["y"], delay=randint(*delay))

        except PlaywrightTimeoutError:
            raise Exception(f"Element with selector '{selector}' not found for clicking.")

    def human_like_mouse_move(self, start_position: dict, end_position: dict, steps=20):
        self.page.mouse.move(start_position["x"], start_position["y"])
        for i in range(1, steps + 1):
            x = start_position["x"] + (end_position["x"] - start_position["x"]) * i / steps + uniform(-1, 1)
            y = start_position["y"] + (end_position["y"] - start_position["y"]) * i / steps + uniform(-1, 1)
            self.page.mouse.move(x, y)
            self.mouse_position = {"x": x, "y": y}
            time.sleep(uniform(0.01, 0.03))

    def is_element_in_viewport(self, box: dict) -> bool:
        viewport = self.page.viewport_size
        return (
                0 <= box["x"] <= viewport["width"] and
                0 <= box["y"] <= viewport["height"]
        )

    def scroll_to_element_like_human(self, box: dict, step: int = 100):
        current_scroll = self.page.evaluate("() => window.scrollY")
        target_scroll = box["y"] - 200
        direction = 1 if target_scroll > current_scroll else -1

        for scroll_y in range(int(current_scroll), int(target_scroll), direction * step):
            self.page.evaluate(f"() => window.scrollTo(0, {scroll_y})")
            time.sleep(uniform(0.05, 0.15))

        self.page.evaluate(f"() => window.scrollTo(0, {target_scroll})")
        time.sleep(uniform(0.1, 0.2))

    def type(self, selector: str, text: str, timeout: int = TIMEOUT, delay: list = DELAYS['type']):
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.type(selector, text, delay=randint(*delay))
        except PlaywrightTimeoutError:
            raise Exception(f"Element with selector '{selector}' not found for filling.")

    def get_text(self, selector: str, timeout: int = TIMEOUT) -> str:
        return self.page.text_content(selector, timeout=timeout)

    def is_visible(self, selector: str, timeout: int = TIMEOUT) -> bool:
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_url(self, url_part: str, timeout: int = TIMEOUT):
        self.page.wait_for_url(f"**{url_part}**", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = TIMEOUT):
        self.page.wait_for_selector(selector, timeout=timeout)

    def query_selector_all(self, selector: str):
        self.page.query_selector_all(selector)

    def press_key(self, selector: str, key: str, delay: list = DELAYS['click']):
        self.page.press(selector, key, delay=randint(*delay))

