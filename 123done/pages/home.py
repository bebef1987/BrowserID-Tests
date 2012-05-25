#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from page import Page


class HomePage(Page):

    _page_title = '123done - your tasks, simplified'

    _sign_in_locator = (By.CSS_SELECTOR, '#loggedout > button')
    _logout_locator = (By.CSS_SELECTOR, '#loggedin > a')
    _logged_in_user_email_locator = (By.CSS_SELECTOR, '#loggedin > span')
    _loading_spinner_locator = (By.CSS_SELECTOR, "li.loading img")

    def go_to_home_page(self):
        self.selenium.get(self.base_url + '/')
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._sign_in_locator),
            "Sign-in button did not appear before timeout")
        self.is_the_current_page

    def sign_in(self, user='default'):
        credentials = self.testsetup.credentials[user]
        self.click_sign_in()
        from browserid import BrowserID
        browserid = BrowserID(self.selenium, self.timeout)
        browserid.sign_in(credentials['email'], credentials['password'])
        self.wait_for_user_login()

    def logout(self):
        self.click_logout()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: not self.is_element_visible(*self._logout_locator)
            and not self.is_element_visible(*self._loading_spinner_locator),
            "Logout button did not disappear before the timeout")

    def click_sign_in(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        from browserid import BrowserID
        return BrowserID(self.selenium, self.timeout)

    def click_logout(self):
        self.selenium.find_element(*self._logout_locator).click()

    @property
    def is_logged_in(self):
        return self.is_element_visible(*self._logout_locator)

    @property
    def logged_in_user_email(self):
        return self.selenium.find_element(*self._logged_in_user_email_locator).text

    def wait_for_user_login(self):        
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._logout_locator)
            and not self.is_element_visible(*self._loading_spinner_locator),
            "User could not log in before the timeout")
