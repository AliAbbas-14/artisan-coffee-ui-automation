from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for Authentication / Login Page."""

    EMAIL_INPUT = "input[type='email'], input[name='email'], #email"
    PASSWORD_INPUT = "input[type='password'], input[name='password'], #password"
    SUBMIT_BTN = "button[type='submit']"
    ERROR_ALERT = ".text-red-500, .text-destructive, [role='alert']"
    NAV_SIGN_OUT = "button:has-text('Sign out'), text='Sign out'"

    def open(self) -> None:
        self.navigate("/login")

    def login(self, email: str, password: str) -> None:
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_ALERT, timeout=4000)

    def get_error_message(self) -> str:
        if self.is_error_displayed():
            return self.get_text(self.ERROR_ALERT)
        return ""

    def is_logged_in(self) -> bool:
        # Check if redirected to home/menu or Sign out button is present
        return self.is_visible(self.NAV_SIGN_OUT, timeout=6000) or "/login" not in self.get_current_url()
