import time

from core.session import Session
from workflows import AuthFlow, ShopFlow
from data.logger_config import logger
from data.config import ON_PROXY
from faker import Faker

def main():
    logger.info("Створення сессии")
    session = Session()
    session.start()

    auth = AuthFlow(session)
    is_auth = auth.login(username='locked_out_user')
    if not is_auth:
        time.sleep(3)
        session.stop()
        return

    shop = ShopFlow(session)
    shop.add_to_cart(count=1, price={"min": 0, "max": 200})

    faker = Faker()
    shop.purchase(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        postal_code=faker.postalcode(),
    )



if __name__ == "__main__":
    main()