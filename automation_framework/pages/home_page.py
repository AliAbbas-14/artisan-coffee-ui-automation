from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for Artisan Coffee Landing and Hero View."""

    HERO_SECTION = "#hero"
    BRAND_LOGO = ":has-text('ARTISANCOFFEE')"
    NAV_MENU_BTN = "button:has-text('MENU')"
    NAV_STORY_BTN = "button:has-text('STORY')"
    NAV_BLEND_BTN = "button:has-text('BLEND')"
    NAV_REVIEWS_BTN = "button:has-text('REVIEWS')"
    NAV_LOCATIONS_BTN = "button:has-text('LOCATIONS')"
    ORDER_NOW_BTN = "button:has-text('ORDER NOW')"
    EXPLORE_MENU_LINK = "a:has-text('EXPLORE OUR MENU'), a:has-text('VIEW FULL MENU')"
    HERO_RATING_BADGE = ":has-text('Rated Excellent'), :has-text('4.9 ★')"

    def open(self) -> None:
        self.navigate("/")

    def click_menu_nav(self) -> None:
        self.click(self.NAV_MENU_BTN)
        self.page.wait_for_timeout(500)

    def click_story_nav(self) -> None:
        self.click(self.NAV_STORY_BTN)
        self.page.wait_for_timeout(500)

    def click_blend_nav(self) -> None:
        self.click(self.NAV_BLEND_BTN)
        self.page.wait_for_timeout(500)

    def click_locations_nav(self) -> None:
        self.click(self.NAV_LOCATIONS_BTN)
        self.page.wait_for_timeout(500)

    def is_hero_displayed(self) -> bool:
        return self.is_visible(self.HERO_SECTION) or self.is_visible(self.BRAND_LOGO)
