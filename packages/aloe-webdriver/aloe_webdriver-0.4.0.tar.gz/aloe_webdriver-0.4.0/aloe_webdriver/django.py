"""
Django-specific extensions
"""

try:
    from urllib.parse import urljoin  # pylint:disable=no-name-in-module
except ImportError:
    from urlparse import urljoin  # pylint:disable=import-error

from aloe import step

# make sure the steps are loaded
import aloe_webdriver.webdriver  # pylint:disable=unused-import


@step(r'I visit site page "([^"]*)"')
def visit_page(self, page):
    """
    Visit the specific page of the site.
    """

    testclass = self.testclass
    base_url = testclass.live_server_url.__get__(testclass)
    url = urljoin(base_url, page)
    self.given('I visit "%s"' % url)
