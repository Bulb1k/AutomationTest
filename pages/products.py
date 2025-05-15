import time

from core.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, session):
        super().__init__(session)
        self.PRODUCT_LIST = []

    def load_product(self):
        frame = self.page.frame(url="https://www.saucedemo.com/inventory.html")
        frame.wait_for_selector('div.inventory_item')
        products = frame.query_selector_all('div.inventory_item')

        for product in products:
            product_info = {}

            btn_id = product.query_selector('button').get_attribute('id')
            product_info["add_cart_button_id"] = btn_id
            price = product.query_selector('div.inventory_item_price').text_content()
            product_info["price"] = float(price.replace("$", ""))
            name = product.query_selector('div.inventory_item_name').text_content()
            product_info["name"] = name

            self.PRODUCT_LIST.append(product_info)

    def add_product_to_cart(self, product_name: str):
        product = None
        for p in self.PRODUCT_LIST:
            if p["name"] == product_name:
                product = p
                break
        else:
            raise ValueError(f"Product '{product_name}' not found in the product list")


        button_id = product.get('add_cart_button_id')
        if not button_id:
            raise ValueError(f"Product '{product_name}' not found on the page")

        button_id = self.page.evaluate(f"CSS.escape('{button_id}')")

        self.click_by_human(f'button#{button_id}')

    def go_to_cart(self):
        self.click_by_human('a.shopping_cart_link')
        time.sleep(2)
        self.wait_for_selector('div.cart_list')

    def click_checkout(self):
        self.click_by_human('button#checkout')
        time.sleep(2)
        self.wait_for_selector('div.checkout_info')

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        self.type('input#first-name', first_name)
        self.type('input#last-name', last_name)
        self.type('input#postal-code', postal_code)
        self.click_by_human('input#continue')
        time.sleep(2)
        self.wait_for_selector('div.checkout_summary_container')

    def click_finish(self):
        self.click_by_human('button#finish')
        time.sleep(2)
        text_complete = self.page.locator("h2.complete-header").text_content()
        if text_complete == "Thank you for your order!":
            return True
        return ValueError("Order not completed")




