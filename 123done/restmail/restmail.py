#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json
from time import sleep

class RestmailInbox(object):
    
    restmail_mail_server = "https://restmail.net/mail/"
    
    def __init__(self, email):
        self.email = email
        self.username = email.split('@')[0]
        self.json = self._wait_and_return_json_response(self.username)

    def _wait_and_return_json_response(self, username, timeout=60):
        timer = 0
        response_json = []
        
        while timer < timeout:        
            sleep(1)
            timer += 1

            response = requests.get(self.restmail_mail_server + self.username, verify=False)
            response_json = json.loads(response.content)
            if response_json != []:
                return response_json

        else:
            raise Exception("Failed to find email before timeout")

    def delete_all_mail(self):
        requests.delete(self.restmail_mail_server + self.username, verify=False)

    def find_by_index(self, index):
        return EMail(self.json[index])

    def find_by_sender(self, sender):
        for json_object in self.json:
            for from_source in json_object['from']:
                if from_source['address'] == sender or from_source['name'] == sender:
                    return EMail(json_object)
        else:
            raise Exception("Sender not found")

class EMail():

    def __init__(self, json):
        self.json = json

    @property
    def body(self):
        return(self.json['text'])

    @property
    def bid_link(self):
        body = self.json['text']
        start = body.find('https')
        end = body.find('\n\nIf')
        return body[start:end]
