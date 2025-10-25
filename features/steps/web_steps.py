"""Web UI step definitions (Selenium-based stubs).

These steps are generic and can be adapted to your specific admin UI
by adjusting selectors. They assume `context.browser` is a Selenium
WebDriver instance configured elsewhere (e.g., in environment.py).
"""

from behave import then, when


def _require_browser(context):
    if not hasattr(context, "browser") or context.browser is None:
        raise RuntimeError(
            "context.browser is not set. Initialize a Selenium WebDriver in environment.py."
        )


@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    _require_browser(context)
    # Try by <button> text, then by input[value], then fallback by id
    browser = context.browser
    candidates = [
        f'//button[normalize-space()="{button_text}"]',
        f'//input[@type="submit" and @value="{button_text}"]',
        f'//*[@id="{button_text}"]',
        f'//*[@data-test="{button_text}"]',
    ]
    for xpath in candidates:
        found = browser.find_elements("xpath", xpath)
        if found:
            found[0].click()
            return
    raise AssertionError(f"Button with text/id '{button_text}' not found")


@then('I should see "{text}"')
def step_should_see_text(context, text):
    _require_browser(context)
    page = context.browser.page_source
    assert text in page, f"Expected to see '{text}' in page"


@then('I should not see "{text}"')
def step_should_not_see_text(context, text):
    _require_browser(context)
    page = context.browser.page_source
    assert text not in page, f"Did not expect to see '{text}' in page"


@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    _require_browser(context)
    # Try a few common message containers (e.g., flash, alert, toast)
    browser = context.browser
    xpaths = [
        '//*[@id="flash_message"]',
        '//*[@role="alert"]',
        '//*[contains(@class, "alert")]',
        '//*[contains(@class, "toast")]',
    ]
    for xp in xpaths:
        elems = browser.find_elements("xpath", xp)
        if elems and any(message in e.text for e in elems):
            return
    # Fallback to page source
    assert message in browser.page_source, f"Expected message '{message}'"
