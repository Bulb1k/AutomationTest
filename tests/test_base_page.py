import time

from core.base_page import BasePage
from data.config import DEFAULT_SITE_URLS
import pytest

@pytest.mark.skip(reason="Skip test base_page")
def base_page(session):
    assert session is not None

    base_page = BasePage(session)
    base_page.go_to(DEFAULT_SITE_URLS['default'])
    assert "Swag Labs" in base_page.page.title()
    yield base_page


@pytest.mark.skip(reason="Skip test base_page")
def test_base_page_click(session, base_page):
    base_page.go_to(DEFAULT_SITE_URLS['default'])

    selector = 'input#login-button'
    base_page.click_by_human(selector)
    time.sleep(3)