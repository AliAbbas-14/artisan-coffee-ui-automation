import os
import sys
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK_ROOT = os.path.dirname(CURRENT_DIR)
if FRAMEWORK_ROOT not in sys.path:
    sys.path.insert(0, FRAMEWORK_ROOT)

from config.config import Config
from pages.home_page import HomePage
from pages.menu_page import MenuPage
from pages.blend_page import BlendPage
from pages.newsletter_page import NewsletterPage
from pages.locations_page import LocationsPage
from data.data_manager import DataManager

def before_all(context):
    """Launch Playwright browser instance."""
    context.playwright = sync_playwright().start()
    browser_type = getattr(context.playwright, Config.BROWSER_TYPE, context.playwright.chromium)
    context.browser = browser_type.launch(
        headless=Config.HEADLESS
    )
    context.data_mgr = DataManager()
    print(f"\n[PLAYWRIGHT INIT] Engine: {Config.BROWSER_TYPE.upper()} | Headless: {Config.HEADLESS}")

def before_scenario(context, scenario):
    """Fresh isolated browser page context for every scenario."""
    context.browser_context = context.browser.new_context(
        viewport={"width": Config.VIEWPORT_WIDTH, "height": Config.VIEWPORT_HEIGHT},
        ignore_https_errors=True
    )
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(Config.DEFAULT_TIMEOUT)

    # Initialize Page Objects
    context.home_page = HomePage(context.page, Config.BASE_URL)
    context.menu_page = MenuPage(context.page, Config.BASE_URL)
    context.blend_page = BlendPage(context.page, Config.BASE_URL)
    context.newsletter_page = NewsletterPage(context.page, Config.BASE_URL)
    context.locations_page = LocationsPage(context.page, Config.BASE_URL)

def after_step(context, step):
    """Capture screenshot on failure and attach to Allure."""
    if step.status == "failed":
        try:
            screenshot = context.page.screenshot(full_page=False)
            allure.attach(
                screenshot,
                name=f"FAIL_{step.name[:30]}",
                attachment_type=AttachmentType.PNG
            )
        except Exception:
            pass

def after_scenario(context, scenario):
    """Capture scenario completion screenshot and tear down context."""
    try:
        screenshot = context.page.screenshot(full_page=False)
        allure.attach(
            screenshot,
            name=f"SCENARIO_{scenario.name[:30]}",
            attachment_type=AttachmentType.PNG
        )
    except Exception:
        pass

    if hasattr(context, "page") and context.page:
        context.page.close()
    if hasattr(context, "browser_context") and context.browser_context:
        context.browser_context.close()

def after_all(context):
    """Clean up browser process."""
    if hasattr(context, "browser") and context.browser:
        context.browser.close()
    if hasattr(context, "playwright") and context.playwright:
        context.playwright.stop()
    print("\n[PLAYWRIGHT TEARDOWN] Cleaned up browser sessions.")
