from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import geckodriver_autoinstaller
geckodriver_autoinstaller.install()

import time

class SeleniumTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()
        self.root_url = self.live_server_url

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_welcome(self):
        self.browser.get(self.live_server_url + '/welcome/')
        self.assertRegex(self.browser.page_source, "[w,W]elcome\\s+to\\s+[m,M]y\\s+[l,L]ibrary")
        self.assertRegex(self.browser.page_source, f'href=\"[{self.live_server_url}/]books/\"')

    def test_create_book(self):
        self.browser.get(self.live_server_url + '/create_book/')
        actual_url = self.browser.current_url
        expected_url = self.root_url+'/create_book/'
        self.assertEqual(expected_url, actual_url)
        ... # first (invalid) form submission
        actual_url = self.browser.current_url
        expected_url = self.root_url+'/create_book/'
        self.assertEqual(expected_url, actual_url)
        ... # second (valid) form submission
        actual_url = self.browser.current_url
        expected_url = self.root_url+'/books/'
        self.assertEqual(expected_url, actual_url)