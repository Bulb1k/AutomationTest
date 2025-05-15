import time
import pytest
from workflows import AuthFlow

# @pytest.mark.skip(reason="Skip test")
def test_login(session):
    auth_flow = AuthFlow(session)
    assert auth_flow is not None
    assert auth_flow.login()


@pytest.mark.skip(reason="Skip test")
def test_fail_login(session):
    auth_flow = AuthFlow(session)
    assert auth_flow is not None
    auth_flow.login(username='invalid_user', password='invalid_password')
    time.sleep(5)
