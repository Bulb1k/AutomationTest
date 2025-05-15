import time
import pytest
from workflows import ShopFlow

@pytest.mark.skip(reason="Skip test")
def test_add_cart(session):
    shop_flow = ShopFlow(session)
    assert shop_flow is not None
    shop_flow.add_to_cart(count=5)

@pytest.mark.skip(reason="Skip test")
def test_purchase(session):
    shop_flow = ShopFlow(session)
    assert shop_flow is not None
    shop_flow.purchase()