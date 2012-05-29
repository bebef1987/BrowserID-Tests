#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home import HomePage
from pages.bid import Bid
from restmail.restmail import RestmailInbox
from mocks.mock_user import MockUser
from unittestzero import Assert

import pytest


class TestNewAccount:

    def test_can_create_new_user_account(self, mozwebqa):
        user = MockUser()
        home_pg = HomePage(mozwebqa)

        home_pg.go_to_home_page()
        bid_login = home_pg.click_sign_in("new")
        bid_login.sign_in_new_user(user['email'])

        # Open restmail inbox, find the email
        inbox = RestmailInbox(user['email'])
        email = inbox.find_by_sender('BrowserID@browserid.org')

        # Load the BrowserID link from the email in the browser
        mozwebqa.selenium.get(email.bid_link)
        verify_email_address = Bid.VerifyEmailAddress(mozwebqa.selenium, mozwebqa.timeout)

        verify_email_address.verify_email_address(user['password'])

        home_pg.go_to_home_page()
        bid_login = home_pg.click_sign_in("returning")
        Assert.equal(user['email'], bid_login.email)

        bid_login.sign_in_returning_user()
        home_pg.wait_for_user_login()

        Assert.equal(home_pg.logged_in_user_email, user['email'])
