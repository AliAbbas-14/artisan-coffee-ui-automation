from pages.base_page import BasePage

class NewsletterPage(BasePage):
    """Page Object for Newsletter Subscription Form Automation."""

    NEWSLETTER_CONTAINER = "section:has-text('THE COFFEE LETTER'), div:has-text('THE COFFEE LETTER')"
    EMAIL_INPUT = "input[type='email'], input[placeholder='your@email.com']"
    SUBSCRIBE_BTN = "button:has-text('SUBSCRIBE')"

    def open(self) -> None:
        self.navigate("/")

    def enter_email(self, email: str) -> None:
        self.page.locator(self.EMAIL_INPUT).scroll_into_view_if_needed()
        self.fill(self.EMAIL_INPUT, email)

    def click_subscribe(self) -> None:
        self.click(self.SUBSCRIBE_BTN)
        self.page.wait_for_timeout(600)

    def is_form_present(self) -> bool:
        return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.SUBSCRIBE_BTN)

    def get_input_value(self) -> str:
        return self.page.locator(self.EMAIL_INPUT).input_value()
