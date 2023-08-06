"""Webdriver support for Aloe"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# pylint:disable=redefined-builtin
from builtins import str
# pylint:enable=redefined-builtin

from aloe import step, world

from aloe_webdriver.util import (
    find_any_field,
    find_button,
    find_field,
    find_option,
    option_in_select,
    wait_for,
)

from nose.tools import (
    assert_equal,
    assert_false,
    assert_in,
    assert_not_in,
    assert_true,
)

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
    WebDriverException)

# pylint:disable=missing-docstring

# pylint:disable=wildcard-import,unused-wildcard-import
from aloe_webdriver.css_selector_steps import *
# pylint:enable=wildcard-import,unused-wildcard-import


def contains_content(browser, content):
    # Search for an element that contains the whole of the text we're looking
    #  for in it or its subelements, but whose children do NOT contain that
    #  text - otherwise matches <body> or <html> or other similarly useless
    #  things.
    for elem in browser.find_elements_by_xpath(str(
            '//*[contains(normalize-space(.),"{content}") '
            'and not(./*[contains(normalize-space(.),"{content}")])]'
            .format(content=content))):

        try:
            if elem.is_displayed():
                return True
        except StaleElementReferenceException:
            pass

    return False


@wait_for
def wait_for_elem(browser, xpath):
    return browser.find_elements_by_xpath(str(xpath))


@wait_for
def wait_for_content(browser, content):
    return contains_content(browser, content)


# URLS
@step('I visit "(.*?)"$')
def visit(self, url):
    world.browser.get(url)


@step('I go to "(.*?)"$')
def goto(self, url):
    self.given('I visit "%s"' % url)


# Links
@step('I click "(.*?)"$')
def click(self, name):
    elem = world.browser.find_element_by_link_text(name)
    elem.click()


@step('I should see a link with the url "(.*?)"$')
def should_see_link(self, link_url):
    assert_true(world.browser.
                find_element_by_xpath(str('//a[@href="%s"]' % link_url)))


@step('I should see a link to "(.*?)" with the url "(.*?)"$')
def should_see_link_text(self, link_text, link_url):
    assert_true(world.browser.find_element_by_xpath(str(
        '//a[@href="%s"][./text()="%s"]' %
        (link_url, link_text))))


@step('I should see a link that contains the text "(.*?)" '
      'and the url "(.*?)"$')
def should_include_link_text(self, link_text, link_url):
    return world.browser.find_element_by_xpath(str(
        '//a[@href="%s"][contains(., "%s")]' %
        (link_url, link_text)))


# General
@step('The element with id of "(.*?)" contains "(.*?)"$')
def element_contains(self, element_id, value):
    return world.browser.find_element_by_xpath(str(
        'id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value)))


@step('The element with id of "(.*?)" does not contain "(.*?)"$')
def element_not_contains(self, element_id, value):
    elem = world.browser.find_elements_by_xpath(str(
        'id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value)))
    assert_false(elem)


@wait_for
def wait_for_visible_elem(browser, xpath):
    elem = browser.find_elements_by_xpath(str(xpath))
    if not elem:
        return False
    return elem[0].is_displayed()


@step(r'I should see an element with id of "(.*?)" within (\d+) seconds?$')
def should_see_id_in_seconds(self, element_id, timeout):
    # pylint:disable=unexpected-keyword-arg
    # wait_for decorator parses the argument
    elem = wait_for_visible_elem(world.browser, 'id("%s")' % element_id,
                                 timeout=int(timeout))
    assert_true(elem)


@step('I should see an element with id of "(.*?)"$')
def should_see_id(self, element_id):
    elem = world.browser.find_element_by_xpath(str('id("%s")' % element_id))
    assert_true(elem.is_displayed())


@step('I should not see an element with id of "(.*?)"$')
def should_not_see_id(self, element_id):
    try:
        elem = world.browser.find_element_by_xpath(str('id("%s")' %
                                                       element_id))
        assert_false(elem.is_displayed())
    except NoSuchElementException:
        pass


@step(r'I should see "([^"]+)" within (\d+) seconds?$')
def should_see_in_seconds(self, text, timeout):
    # pylint:disable=unexpected-keyword-arg
    # wait_for decorator parses the argument
    assert_true(wait_for_content(world.browser, text, timeout=int(timeout)))


@step('I should see "([^"]+)"$')
def should_see(self, text):
    assert_true(contains_content(world.browser, text))


@step('I see "([^"]+)"$')
def see(self, text):
    assert_true(contains_content(world.browser, text))


@step('I should not see "([^"]+)"$')
def should_not_see(self, text):
    assert_false(contains_content(world.browser, text))


@step('I should be at "(.*?)"$')
def url_should_be(self, url):
    assert_equal(url, world.browser.current_url)


# Browser
@step('The browser\'s URL should be "(.*?)"$')
def browser_url_should_be(self, url):
    assert_equal(url, world.browser.current_url)


@step('The browser\'s URL should contain "(.*?)"$')
def url_should_contain(self, url):
    assert_in(url, world.browser.current_url)


@step('The browser\'s URL should not contain "(.*?)"$')
def url_should_not_contain(self, url):
    assert_not_in(url, world.browser.current_url)


# Forms
@step('I should see a form that goes to "(.*?)"$')
def see_form(self, url):
    return world.browser.find_element_by_xpath(str('//form[@action="%s"]' %
                                                   url))


DATE_FIELDS = (
    'datetime',
    'datetime-local',
    'date',
)


TEXT_FIELDS = (
    'text',
    'textarea',
    'password',
    'month',
    'time',
    'week',
    'number',
    'range',
    'email',
    'url',
    'tel',
    'color',
)


@step('I fill in "(.*?)" with "(.*?)"$')
def fill_in_textfield(self, field_name, value):
    date_field = find_any_field(world.browser,
                                DATE_FIELDS,
                                field_name)
    if date_field:
        field = date_field
    else:
        field = find_any_field(world.browser,
                               TEXT_FIELDS,
                               field_name)

    assert_true(field,
                'Can not find a field named "%s"' % field_name)
    if date_field:
        field.send_keys(Keys.DELETE)
    else:
        field.clear()
    field.send_keys(value)


@step('I press "(.*?)"$')
def press_button(self, value):
    button = find_button(world.browser, value)
    button.click()


@step('I click on label "([^"]*)"')
def click_on_label(self, label):
    """
    Click on a label
    """

    elem = world.browser.find_element_by_xpath(str(
        '//label[normalize-space(text()) = "%s"]' % label))
    elem.click()


@step(r'Element with id "([^"]*)" should be focused')
def element_focused(self, id_):
    """
    Check if the element is focused
    """

    elem = world.browser.find_element_by_xpath(
        str('id("{id}")'.format(id=id_)))
    focused = world.browser.switch_to_active_element()

    assert_true(elem == focused)


@step(r'Element with id "([^"]*)" should not be focused')
def element_not_focused(self, id_):
    """
    Check if the element is not focused
    """

    elem = world.browser.find_element_by_xpath(
        str('id("{id}")'.format(id=id_)))
    focused = world.browser.switch_to_active_element()

    # Elements don't have __ne__ defined, cannot test for inequality
    assert_false(elem == focused)


@step(r'Input "([^"]*)" (?:has|should have) value "([^"]*)"')
def input_has_value(self, field_name, value):
    """
    Check that the form input element has given value.
    """
    text_field = find_any_field(world.browser,
                                DATE_FIELDS + TEXT_FIELDS,
                                field_name)
    assert_false(text_field is False,
                 'Can not find a field named "%s"' % field_name)
    assert_equal(text_field.get_attribute('value'), value)


@step(r'I submit the only form')
def submit_the_only_form(self):
    """
    Look for a form on the page and submit it.
    """
    form = world.browser.find_element_by_xpath(str('//form'))
    form.submit()


@step(r'I submit the form with id "([^"]*)"')
def submit_form_id(self, id_):
    """
    Submit the form having given id.
    """
    form = world.browser.find_element_by_xpath(
        str('id("{id}")'.format(id=id_)))
    form.submit()


@step(r'I submit the form with action "([^"]*)"')
def submit_form_action(self, url):
    """
    Submit the form having given action URL.
    """
    form = world.browser.find_element_by_xpath(str('//form[@action="%s"]' %
                                                   url))
    form.submit()


# Checkboxes
@step('I check "(.*?)"$')
def check_checkbox(self, value):
    check_box = find_field(world.browser, 'checkbox', value)
    if not check_box.is_selected():
        check_box.click()


@step('I uncheck "(.*?)"$')
def uncheck_checkbox(self, value):
    check_box = find_field(world.browser, 'checkbox', value)
    if check_box.is_selected():
        check_box.click()


@step('The "(.*?)" checkbox should be checked$')
def assert_checked_checkbox(self, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert_true(check_box.is_selected())


@step('The "(.*?)" checkbox should not be checked$')
def assert_not_checked_checkbox(self, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert_false(check_box.is_selected())


# Selectors
@step('I select "(.*?)" from "(.*?)"$')
def select_single_item(self, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    option_box.click()


@step('I select the following from "([^"]*?)":?$')
def select_multi_items(self, select_name):
    # Ensure only the options selected are actually selected
    option_names = self.multiline.split('\n')
    select_box = find_field(world.browser, 'select', select_name)

    select = Select(select_box)
    select.deselect_all()

    for option in option_names:
        try:
            select.select_by_value(option)
        except NoSuchElementException:
            select.select_by_visible_text(option)


@step('The "(.*?)" option from "(.*?)" should be selected$')
def assert_single_selected(self, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    assert_true(option_box.is_selected())


@step('The following options from "([^"]*?)" should be selected:?$')
def assert_multi_selected(self, select_name):
    # Ensure its not selected unless its one of our options
    option_names = self.multiline.split('\n')
    select_box = find_field(world.browser, 'select', select_name)
    option_elems = select_box.find_elements_by_xpath(str('./option'))
    for option in option_elems:
        if option.get_attribute('id') in option_names or \
           option.get_attribute('name') in option_names or \
           option.get_attribute('value') in option_names or \
           option.text in option_names:
            assert_true(option.is_selected())
        else:
            assert_false(option.is_selected())


@step(r'I should see option "([^"]*)" in selector "([^"]*)"')
def select_contains(self, option, id_):
    assert_true(option_in_select(world.browser, id_, option) is not None)


@step(r'I should not see option "([^"]*)" in selector "([^"]*)"')
def select_does_not_contain(self, option, id_):
    assert_true(option_in_select(world.browser, id_, option) is None)


# Radios
@step('I choose "(.*?)"$')
def choose_radio(self, value):
    box = find_field(world.browser, 'radio', value)
    box.click()


@step('The "(.*?)" option should be chosen$')
def assert_radio_selected(self, value):
    box = find_field(world.browser, 'radio', value)
    assert_true(box.is_selected())


@step('The "(.*?)" option should not be chosen$')
def assert_radio_not_selected(self, value):
    box = find_field(world.browser, 'radio', value)
    assert_false(box.is_selected())


# Alerts
@step('I accept the alert')
def accept_alert(self):
    """
    Accept the alert
    """

    try:
        alert = Alert(world.browser)
        alert.accept()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I dismiss the alert')
def dismiss_alert(self):
    """
    Dismiss the alert
    """

    try:
        alert = Alert(world.browser)
        alert.dismiss()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step(r'I should see an alert with text "([^"]*)"')
def check_alert(self, text):
    """
    Check the alert text
    """

    try:
        alert = Alert(world.browser)
        assert_equal(alert.text, text)
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I should not see an alert')
def check_no_alert(self):
    """
    Check there is no alert
    """

    try:
        alert = Alert(world.browser)
        raise AssertionError("Should not see an alert. Alert '%s' shown." %
                             alert.text)
    except NoAlertPresentException:
        pass


# Tooltips
@step(r'I should see an element with tooltip "([^"]*)"')
def see_tooltip(self, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = world.browser.find_elements_by_xpath(str(
        '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)))
    elem = [e for e in elem if e.is_displayed()]
    assert_true(elem)


@step(r'I should not see an element with tooltip "([^"]*)"')
def no_see_tooltip(self, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = world.browser.find_elements_by_xpath(str(
        '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)))
    elem = [e for e in elem if e.is_displayed()]
    assert_false(elem)


@step(r'I (?:click|press) the element with tooltip "([^"]*)"')
def press_by_tooltip(self, tooltip):
    """
    Press a button having a given tooltip.
    """
    for button in world.browser.find_elements_by_xpath(str(
            '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]'
            % dict(tooltip=tooltip)
    )):
        try:
            button.click()
            break
        except:  # pylint:disable=bare-except
            pass
    else:
        raise AssertionError("No button with tooltip '{0}' found"
                             .format(tooltip))


@step(r'The page title should be "([^"]*)"')
def page_title(self, title):
    """
    Check that the page title matches the given one.
    """
    assert_equal(world.browser.title, title)


@step(r'I switch to the frame with id "([^"]*)"')
def switch_to_frame(self, frame):
    elem = world.browser.find_element_by_id(frame)
    world.browser.switch_to_frame(elem)


@step(r'I switch back to the main view')
def switch_to_main(self):
    world.browser.switch_to_default_content()
