import pytest
from playwright.sync_api import expect

import config
from pages.login_page import LoginPage
from tests.data.users import USERS

pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    "username, password",
    [
        ("", ""),
        (USERS["standard"], "wrong_password"),
        ("fake_user", config.PASSWORD),
    ],
    ids=["empty_credentials", "real_user_wrong_password", "fake_user_real_password"],
)
def test_login_with_invalid_credentials(page, username, password):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(page).to_have_url(LoginPage.URL)
