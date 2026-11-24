from behave import when, then

@when('the user navigates to the signature menu section')
def step_nav_to_menu_section(context):
    context.menu_page.open()
    context.page.wait_for_timeout(500)

@then('the signature menu header should be displayed')
def step_assert_menu_header(context):
    assert context.menu_page.is_menu_section_visible(), "Signature menu header is not visible"

@then('the menu should feature "{coffee_name}"')
def step_assert_menu_product(context, coffee_name):
    assert context.menu_page.has_product(coffee_name), f"Product '{coffee_name}' not found in menu"

@then('the coffee origin "{origin}" should be displayed in the menu')
def step_assert_coffee_origin(context, origin):
    menu_text = context.menu_page.get_menu_text()
    assert origin in menu_text, f"Origin '{origin}' not found in menu text"
