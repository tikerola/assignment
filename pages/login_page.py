"""Login page (`/`)."""


class LoginPage:
    URL = "/"

    def __init__(self, page):
        self.page = page

    def open(self):
        # Resolves against pytest.ini's base_url setting, not a hardcoded absolute URL.
        self.page.goto(self.URL)

    @property
    def username_input(self):
        return self.page.get_by_test_id("username")

    @property
    def password_input(self):
        return self.page.get_by_test_id("password")

    @property
    def login_button(self):
        return self.page.get_by_test_id("login-button")

    @property
    def error_message(self):
        return self.page.get_by_test_id("error")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
