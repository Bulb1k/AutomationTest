import time

import pytest
from core.session import Session
from utils.helpers import get_proxies
from random import choice

@pytest.fixture(scope="session")
def session():
    proxy_list = get_proxies()
    proxy = choice(proxy_list)
    session = Session(proxy=proxy)
    session.start()
    yield session
    session.stop()

