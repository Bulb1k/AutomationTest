from pages import ProductsPage
from data.logger_config import logger
import random
import os
import datetime
from data.config import DO_SCREENSHOT

class ShopFlow:
    def __init__(self, session):
        self.session = session
        self.products_page = ProductsPage(session)

    def add_to_cart(self, count: int = 1, price=None):
        if price is None:
            price = {"min": 0, "max": 999999}

        try:
            self.products_page.load_product()
            for _ in range(count):
                product_list = self.products_page.PRODUCT_LIST
                product = random.choice(product_list)
                if price["min"] <= product['price'] <= price["max"]:
                    self.products_page.add_product_to_cart(product['name'])
                    product_list.remove(product)
            logger.info(f"🛒 Додано до кошика {count} товарів у діапазоні цін {price['min']}-{price['max']}.")
            return {"status": "success"}

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"❌ Помилка при додаванні товарів у кошик: {error_type} - {str(e)}")

            screenshot_path = None
            if DO_SCREENSHOT:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/error/add_to_cart_error_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                os.makedirs("screenshots/error", exist_ok=True)
                self.session.current_page.screenshot(path=screenshot_path)
                logger.info(f"📸 Скріншот збережено: {screenshot_path}")

            return {
                "status": "error",
                "error_type": error_type,
                "message": str(e),
                "screenshot": screenshot_path
            }

    def purchase(self, first_name: str = "Test", last_name: str = "Test", postal_code: str = "12345"):
        try:
            self.products_page.go_to_cart()
            self.products_page.click_checkout()
            self.products_page.fill_checkout_form(first_name, last_name, postal_code)
            self.products_page.click_finish()

            screenshot_path = None
            if DO_SCREENSHOT:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/success/purchase_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                os.makedirs("screenshots/success", exist_ok=True)
                self.session.current_page.screenshot(path=screenshot_path)
                logger.info(f"📸 Скріншот збережено: {screenshot_path}")

            logger.info("🛒 Покупка завершена успішно.")
            return {"status": "success"}

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"❌ Помилка при покупці: {error_type} - {str(e)}")

            screenshot_path = None
            if DO_SCREENSHOT:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = f"screenshots/error/purchase_error_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                os.makedirs("screenshots/error", exist_ok=True)
                self.session.current_page.screenshot(path=screenshot_path)
                logger.info(f"📸 Скріншот збережено: {screenshot_path}")

            return {
                "status": "error",
                "error_type": error_type,
                "message": str(e),
                "screenshot": screenshot_path,
            }
