#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from selenium.webdriver.common.by import By



from pages.page import Page


class Base(Page):

    _auth_locator = (By.CSS_SELECTOR, 'div.display_auth')
    _nonauth_locator = (By.CSS_SELECTOR, 'div.display_nonauth')

    @property
    def header(self):
        return Header(self.testsetup)

    def login(self, user='default', use_return=True):
        sign_in = self.header.click_sign_in()
        credentials = self.testsetup.credentials[user]
        sign_in.login(credentials, use_return)

        self.wait_for_element_visible(*self._auth_locator)
        from pages.home import Home
        return Home(self.testsetup , open_url=False)

class Header(Base):

    _sign_in_locator = (By.CSS_SELECTOR, '#header > ul.nav.cf > li.signIn > a')
    _sign_out_locator = (By.CSS_SELECTOR, '#header > ul.nav.cf > li.signOut > a')

    def click_sign_in(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        from pages.sign_in import SignIn
        return SignIn(self.testsetup)

    def click_sign_out(self):
        self.selenium.find_element(*self._sign_out_locator).click()
        self.wait_for_element_visible(*self._nonauth_locator)
        from pages.home import Home
        return Home(self.testsetup, open_url=False)

    @property
    def is_sign_out_visible(self):
        return self.is_element_visible(*self._sign_out_locator)
