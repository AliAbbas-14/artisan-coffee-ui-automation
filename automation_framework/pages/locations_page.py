from pages.base_page import BasePage

class LocationsPage(BasePage):
    """Page Object for Store Locations and Directions."""

    LOCATIONS_SECTION = "#locations"
    LAHORE_BRANCH = "text='Gulberg III, MM Alam Road'"
    DIRECTIONS_BTN = "button:has-text('GET DIRECTIONS')"

    def open(self) -> None:
        self.navigate("/#locations")

    def is_locations_section_visible(self) -> bool:
        return self.is_visible(self.LOCATIONS_SECTION)

    def has_branch(self, branch_name: str) -> bool:
        return self.is_visible(f"text*='{branch_name}'")
