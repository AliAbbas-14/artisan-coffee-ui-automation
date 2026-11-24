from behave import when, then

@then('the newsletter subscription form should be visible')
def step_assert_newsletter_form(context):
    assert context.newsletter_page.is_form_present(), "Newsletter subscription form is not visible"

@then('the email input field and subscribe button should be ready for input')
def step_assert_form_inputs_ready(context):
    assert context.page.locator(context.newsletter_page.EMAIL_INPUT).is_enabled(), "Email input is disabled"
    assert context.page.locator(context.newsletter_page.SUBSCRIBE_BTN).is_enabled(), "Subscribe button is disabled"

@when('the user enters "{email}" into the newsletter subscription input')
def step_enter_newsletter_email(context, email):
    context.newsletter_page.enter_email(email)

@then('the email input field should contain "{email}"')
def step_verify_input_value(context, email):
    val = context.newsletter_page.get_input_value()
    assert val == email, f"Expected input value '{email}', got '{val}'"

@then('the user clicks the subscribe button')
def step_click_subscribe_btn(context):
    context.newsletter_page.click_subscribe()
