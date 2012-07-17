#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
from restmail.restmail import RestmailInbox
from mocks.mock_user import MockUser
from pages.home import HomePage


class TestAddAnotherEmail:

    def test_can_add_another_email(self, mozwebqa):
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
        complete_registration = CompleteRegistration(mozwebqa.selenium, mozwebqa.timeout)

        # Check the message on the registration page reflects a successful registration!
        Assert.contains("Thank you for signing up with Persona.", complete_registration.thank_you)

        home_pg.wait_for_user_login()
        Assert.equal(home_pg.logged_in_user_email, user['email'])

        home_pg.click_logout()

        second_user = MockUser()
        bid_login = home_pg.click_sign_in(expect='returning')
        bid_login.sign_in_add_another_email(second_user['email'])

        # Open restmail inbox, find the email
        inbox = RestmailInbox(second_user['email'])
        email = inbox.find_by_index(0)

        # Load the BrowserID link from the email in the browser
        mozwebqa.selenium.get(email.add_email_address_link)
        from browserid.pages.webdriver.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(mozwebqa.selenium, mozwebqa.timeout)

        home_pg.wait_for_user_login()
        Assert.equal(home_pg.logged_in_user_email, second_user['email'])
        home_pg.click_logout()

        bid_login = home_pg.click_sign_in(expect='returning')
        
        expected_emails = [user['email'], second_user['email']]
        Assert.equal(expected_emails, bid_login.emails)
        Assert.equal(second_user['email'], bid_login.selected_email)
