#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home import HomePage
from restmail.restmail import RestmailInbox
from mocks.mock_user import MockUser
from unittestzero import Assert

import pytest


class TestChangePassword:

    def test_can_change_user_password(self, mozwebqa):
        user = MockUser()
        home_pg = HomePage(mozwebqa)

        home_pg.go_to_home_page()
        bid_login = home_pg.click_sign_in()
        bid_login.sign_in_new_user(user['email'], user['password'])

        # Open restmail inbox, find the email
        inbox = RestmailInbox(user['email'])
        email = inbox.find_by_index(0)

        # Load the BrowserID link from the email in the browser
        mozwebqa.selenium.get(email.verify_user_link)
        from browserid.pages.webdriver.complete_registration import CompleteRegistration
        CompleteRegistration(mozwebqa.selenium, mozwebqa.timeout)

        mozwebqa.selenium.get(mozwebqa.server_base_url)
        from browserid.pages.webdriver.account_manager import AccountManager
        account_manager = AccountManager(mozwebqa.selenium, mozwebqa.timeout)

        Assert.contains(user['email'], account_manager.emails)

        account_manager.click_edit_password()
        account_manager.old_password = user['password']
        new_password = "newpass12345"
        account_manager.new_password = new_password
        account_manager.click_password_done()

        account_manager.click_sign_out()

        home_pg.go_to_home_page()

        bid_login = home_pg.click_sign_in()
        bid_login.sign_in(user['email'], new_password)

        home_pg.wait_for_user_login()
        Assert.true(home_pg.is_logged_in)
