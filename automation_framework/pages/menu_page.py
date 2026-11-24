from pages.base_page import BasePage

class MenuPage(BasePage):
    """Page Object for Artisan Coffee Signature Menu Section."""

    MENU_SECTION = "#menu"
    SECTION_HEADING = "text='OUR SIGNATURE MENU'"
    MENU_ITEMS = "#menu div:has-text('$')"
    ESPRESSO_ITEM = "text='Black Label Espresso'"
    LATTE_ITEM = "text='Velvet Oat Latte'"
    COLD_BREW_ITEM = "text='Midnight Cold Brew'"
    POUR_OVER_ITEM = "text='Pour Over Reserve'"

    def open(self) -> None:
        self.navigate("/#menu")

    def is_menu_section_visible(self) -> bool:
        return self.is_visible(self.MENU_SECTION, timeout=8000)

    def has_product(self, product_name: str) -> bool:
        selector = f"#menu :has-text('{product_name}')"
        return self.is_visible(selector, timeout=5000)

    def get_menu_text(self) -> str:
        return self.get_text(self.MENU_SECTION)
