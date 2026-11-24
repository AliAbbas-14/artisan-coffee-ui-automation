import os
from playwright.sync_api import Page, Locator, expect

class BasePage:
    """Base class for all Page Objects providing reusable Playwright interactions."""

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate(self, path: str = "") -> None:
        """Navigate to relative path or full URL."""
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{self.base_url}/{path.lstrip('/')}"
        self.page.goto(url, wait_until="domcontentloaded")

    def click(self, selector: str, timeout: int = 10000) -> None:
        """Wait for an element to be visible and click it."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.click(selector)

    def fill(self, selector: str, value: str, timeout: int = 10000) -> None:
        """Clear and type into an input field."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.fill(selector, value)

    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get trimmed inner text of an element."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return (self.page.inner_text(selector) or "").strip()

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible within timeout."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, fragment: str, timeout: int = 15000) -> bool:
        """Wait until the browser URL contains the fragment."""
        try:
            self.page.wait_for_url(lambda u: fragment in u, timeout=timeout)
            return True
        except Exception:
            return fragment in self.page.url

    def take_screenshot(self, filepath: str) -> bytes:
        """Capture screenshot to file and return binary bytes."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        return self.page.screenshot(path=filepath, full_page=True)

    def get_title(self) -> str:
        """Return page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return current URL."""
        return self.page.url
