from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for Cart and Checkout Flow."""

    CART_NAV_ICON = "a[href='/cart']"
    CART_ITEMS = ".cart-item, [data-testid='cart-item'], div:has-text('Subtotal')"
    CHECKOUT_BTN = "button:has-text('Place Order'), button:has-text('Checkout'), button:has-text('Proceed')"
    ORDER_SUCCESS_MSG = "text*='Order placed', text*='Thank you', text*='successful'"

    def open(self) -> None:
        self.navigate("/cart")

    def click_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)

    def is_order_successful(self) -> bool:
        return self.is_visible(self.ORDER_SUCCESS_MSG, timeout=6000)
