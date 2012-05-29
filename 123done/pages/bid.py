#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Bid():

    class SignIn():

        def __init__(self, selenium, timeout=60, action="new"):
            self.selenium = selenium
            self.timeout = timeout
            self.action = action
            from browserid.pages.webdriver.sign_in import SignIn
            self.page_object = SignIn(self.selenium, self.timeout, self.action)

        def sign_in(self, email, password):
            self.page_object.sign_in(email, password)

        def sign_in_new_user(self, email):
            self.page_object.sign_in_new_user(email)

        def sign_in_returning_user(self):
            self.page_object.sign_in_returning_user()

        @property
        def email(self):
            # Please repair this in the future when the bidpom email getter is
            # repaired for returning users
            if self.action == "new":
                return self.page_object.email()
            elif self.action == "returning":
                return self.page_object.selenium.find_element(By.CSS_SELECTOR, "label[for='email_0']").text

    class VerifyEmailAddress():

        def __init__(self, selenium, timeout=60):
            self.selenium = selenium
            self.timeout = timeout
            from browserid.pages.webdriver.verify_email_address import VerifyEmailAddress
            self.page_object = VerifyEmailAddress(self.selenium, self.timeout)

        def verify_email_address(self, password):
            self.page_object.verify_email_address(password)
