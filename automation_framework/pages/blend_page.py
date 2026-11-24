from pages.base_page import BasePage

class BlendPage(BasePage):
    """Page Object for The Blend Lab Flavour Profiles section."""

    BLEND_SECTION = "#blend"
    HEADING = "text='THE BLEND LAB'"
    ORDER_ESPRESSO_NOIR = "button:has-text('ORDER ESPRESSO NOIR')"
    ORDER_MORNING_GOLD = "button:has-text('ORDER MORNING GOLD')"
    ORDER_VELVET_HOUR = "button:has-text('ORDER VELVET HOUR')"

    def open(self) -> None:
        self.navigate("/#blend")

    def is_blend_section_visible(self) -> bool:
        return self.is_visible(self.BLEND_SECTION)

    def order_blend(self, blend_name: str) -> None:
        selector = f"button:has-text('ORDER {blend_name.upper()}')"
        self.click(selector)
