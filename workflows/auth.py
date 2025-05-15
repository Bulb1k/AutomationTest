from pages import LoginPage
from data.config import USERNAME, PASSWORD, DO_SCREENSHOT
from data.logger_config import logger
import os
import datetime

class AuthFlow:
    def __init__(self, session):
        self.session = session
        self.login_page = LoginPage(session)

    def login(self, username=USERNAME, password=PASSWORD) -> bool:
        try:
            self.login_page.go_default_page()
            self.login_page.fill_username(username)
            self.login_page.fill_password(password)
            self.login_page.click_login()

            text_error_message = self.login_page.get_text_error_message_container()
            if text_error_message == "":
                logger.info(f"Успішний вхід користувача '{username}'")
                return True
            else:
                logger.warning(f"Помилка входу користувача '{username}': {text_error_message}")
                raise Exception(text_error_message)

        except Exception as e:
            type_error = type(e).__name__
            error_message = str(e)

            logger.error(f"Помилка типу {type_error} під час логіну: {error_message}")

            if DO_SCREENSHOT:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/error/login_error_{timestamp}.png"
                os.makedirs("screenshots/error", exist_ok=True)
                self.session.current_page.screenshot(path=screenshot_path)
                logger.info(f"📸 Скріншот збережено: {screenshot_path}")

            return False

    def logout(self):
        self.login_page.go_default_page()

    def register(self):
        pass
