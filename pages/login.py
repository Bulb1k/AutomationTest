from core.base_page import BasePage
from data.config import DEFAULT_SITE_URLS

class LoginPage(BasePage):
    username_input = "input#user-name"
    password_input = "input#password"
    login_bt = "input#login-button"

    error_message_container = "div.error-message-container.error"

    def fill_username(self, username: str):
        self.type(self.username_input, username)

    def fill_password(self, password: str):
        self.type(self.password_input, password)

    def click_login(self):
        self.click_by_human(self.login_bt)

    def go_default_page(self):
        self.go_to(DEFAULT_SITE_URLS["default"])

    def get_text_error_message_container(self):
        try:
            return self.get_text(self.error_message_container, timeout=100)
        except:
            return ""