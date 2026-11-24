from behave import when, then

@when('the user navigates to the Blend Lab section')
def step_nav_blend_lab(context):
    context.blend_page.open()
    context.page.wait_for_timeout(500)

@then('the Blend Lab section should be visible')
def step_assert_blend_visible(context):
    assert context.blend_page.is_blend_section_visible(), "Blend Lab section is not visible"

@then('the order button for blend "{blend_name}" should be available')
def step_assert_blend_order_btn(context, blend_name):
    selector = f"button:has-text('ORDER {blend_name.upper()}')"
    assert context.blend_page.is_visible(selector, timeout=5000), f"Order button for blend '{blend_name}' is not visible"
