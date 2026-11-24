from pages.base_page import BasePage

class RegisterPage(BasePage):
    """Page Object for User Registration Page."""

    NAME_INPUT = "input[name='name'], input[placeholder*='name' i]"
    EMAIL_INPUT = "input[type='email'], input[name='email']"
    PASSWORD_INPUT = "input[type='password'], input[name='password']"
    SUBMIT_BTN = "button[type='submit']"
    SUCCESS_REDIRECT_OR_MSG = "text='Sign in', text='Login', text='Welcome'"

    def open(self) -> None:
        self.navigate("/register")

    def register(self, name: str, email: str, password: str) -> None:
        if self.is_visible(self.NAME_INPUT, timeout=2000):
            self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
