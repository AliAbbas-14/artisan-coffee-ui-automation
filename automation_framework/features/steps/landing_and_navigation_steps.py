from behave import given, when, then

@given('the user navigates to the Artisan Coffee website')
def step_nav_artisan_coffee(context):
    context.home_page.open()
    context.page.wait_for_load_state("domcontentloaded")

@then('the brand logo "{brand_name}" should be visible')
def step_assert_brand_logo(context, brand_name):
    selector = f":has-text('{brand_name}')"
    assert context.home_page.is_visible(selector, timeout=8000), f"Brand '{brand_name}' not visible"

@then('the page title should contain "{expected_title}"')
def step_assert_page_title(context, expected_title):
    title = context.home_page.get_title()
    assert expected_title.lower() in title.lower(), f"Expected '{expected_title}' in title, got '{title}'"

@then('the hero rating badge should be displayed')
def step_assert_hero_rating(context):
    assert context.home_page.is_visible(context.home_page.HERO_RATING_BADGE, timeout=5000), "Hero rating badge not visible"

@when('the user clicks the navigation button "{nav_button}"')
def step_click_nav_btn(context, nav_button):
    selector = f"button:has-text('{nav_button}')"
    context.home_page.click(selector)
    context.page.wait_for_timeout(500)

@then('the corresponding section "{section_id}" should be displayed')
def step_assert_section_displayed(context, section_id):
    assert context.home_page.is_visible(section_id, timeout=8000), f"Section '{section_id}' is not visible"
