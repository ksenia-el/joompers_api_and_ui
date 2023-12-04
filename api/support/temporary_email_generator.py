# this class used to:
# - generate/create temporary email and password needed to start user registration (in POST /api/registration)
# - check email and return token (extracted from confirmation) needed to complete user registration (in GET /api/email/confirm_email/{token})
# - check email and return confirmation code needed to complete deleting user (in DELETE /api/delete/user/{code})
# - delete temporary email generated before

# (email is created and used by utilizing this service: https://www.1secmail.com/api/)

import requests
import random
import string
import time
import re
from datetime import datetime


class EmailAndPasswordGenerator:

    def __init__(self):
        self.email = None
        self.password = None
        self.api = "https://www.1secmail.com/api/v1/"  # link to the service that generates temporary email


    # method to generate email and password (that used in the endpoint POST /api/registration to create user account)
    # returns two strings: 1) email 2) password - if it was successfully generated;
    # otherwise - returns None for both email and password
    def generate_email_and_password(self):

        #  list of domains used to create an email
        domain_list = [
            "1secmail.com",
            "1secmail.org",
            "1secmail.net"
        ]
        random_domain_from_list = random.choice(domain_list)

        # then we create a username from 10 random symbols (lower case and digits)
        username_symbols = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(username_symbols) for i in range(10))
        self.email = f'{username}@{random_domain_from_list}'  # by that we create email address

        # then we create a password from 8 random symbols (from lower and upper case, and digits)
        password_symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
        self.password = ''.join(random.choice(password_symbols) for i in range(8))

        print(f"Email generated for test user account: {self.email}\nPassword generated for test user account: {self.password}")

        # sending request to log into the email generated - just to check it works
        log_in_response = requests.get(f"{self.api}?login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}")
        assert log_in_response.status_code == 200, "Unknown error. Unable to log into the email generated. Try again"

        return self.email, self.password


    # returns token needed to complete user registration (used in the endpoint GET /api/email/confirm_email/{token})
    # returns one string with the value for "token" - if mail with confirmation link was found in the user email
    # (if multiple mails with confirmation link were received, then it returns the recent one)
    # or returns None as a value for token - if no mail with confirmation link was received
    def get_token_from_confirmation_link_for_registration(self):
        time.sleep(8)  # time gap to wait for new mails to be received, INCREASE IF IT'S NOT ENOUGH
        link_found = None

        # check the email for new mails
        get_mail_response = requests.get(
            f"{self.api}?action=getMessages&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}").json()
        mails_number = len(get_mail_response)

        if mails_number == 0:
            print("No mails in the email detected")

        else:
            # print(f"Number of mails detected in the email: {mails_number}")
            # start to collect IDs of all mails found in the email
            list_of_mails_ids = []
            for mail in get_mail_response:
                for key, value in mail.items():
                    if key == "id":  # the "id" key contains value - ID of a specific email
                        list_of_mails_ids.append(value)  # add ID of a specific mail into a list of all mails from email
            # print(f"The number of mails detected: {mails_number}")

            # finally, analyze every mail in the email - to find those that have a confirmation link inside
            all_links_with_dates_detected = []  # here we will save every confirmation link found + data of receiving it

            for mail_id in list_of_mails_ids:
                get_mail_response = requests.get(
                    f"{self.api}?action=readMessage&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}&id={mail_id}").json()
                sender = get_mail_response.get("from")
                subject = get_mail_response.get("subject")
                date = get_mail_response.get("date")
                content = get_mail_response.get("htmlBody")

                if (sender == "confirm@joompers.com" and subject == "Welcome to Joompers"):
                    pattern_to_look_for = re.search(r'Please confirm your e-mail\s*</h3>\s*<a href="([^"]+)">', content)
                    confirmation_link = pattern_to_look_for.group(1) \
                        if pattern_to_look_for else None  # returns link found - or None if not found
                    if confirmation_link is not None:  # so, if link found
                        # then we get date-time of receiving this link into datetime-object
                        date_parsed = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
                        all_links_with_dates_detected.append((date_parsed, confirmation_link))  # save link + date-time

            if len(all_links_with_dates_detected) == 0:  # if no mail with confirmation link was found
                print(f"No confirmation link for user registration found in email")

            if len(all_links_with_dates_detected) > 1:  # if more then one email with conformation link detected
                # we select the most recent mail (and so the link)
                link_found = max(all_links_with_dates_detected, key=lambda x: x[0])[1]

            else:  # if only one mail with confirmation link was found
                link_found = all_links_with_dates_detected[0][1]

        # print(f"Confirmation link for user registration found: {link_found}")
        # finally, we extract token from the confirmation link received, it's placed in the very end of the link
        token_from_confirmation_link = None
        if link_found is not None:
            token_from_confirmation_link = link_found.split("/")[-1]

        return token_from_confirmation_link


    # returns code neeeded to complete deleting user account (used in the endpoint DELETE /api/delete/user/{code})
    # returns one string with the value for "code" - if mail with code was found in the user email
    # or returns None for "code" - if no mail with code was found
    # (if multiple mails with codes were found in email, then the method returns the most recent one)
    def get_confirmation_code_for_delete_user(self):
        time.sleep(8)
        code_found = None

        # log into the email
        log_in_response = requests.get(f"{self.api}?login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}")

        # check the email for mails
        get_mail_response = requests.get(
            f"{self.api}?action=getMessages&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}").json()
        messages_number = len(get_mail_response)
        # print(f"Number of mails detected in email: {messages_number}")

        if messages_number == 0:
            print("No mails in the email detected")
        else:
            list_of_mails_ids = []
            for mail in get_mail_response:
                for key, value in mail.items():
                    if key == "id":  # the "id" key contains value - ID of a specific mail in the email
                        list_of_mails_ids.append(value)  # add ID of a specific mail into a list of all mails from email
            # print(f"The number of mails detected: {messages_number}")

            # finally, analyze every mail in the email - to find those that have a confirmation code inside
            all_codes_with_dates_detected = []

            for mail_id in list_of_mails_ids:
                get_mail_response = requests.get(
                    f"{self.api}?action=readMessage&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}&id={mail_id}").json()
                sender = get_mail_response.get("from")
                subject = get_mail_response.get("subject")
                date = get_mail_response.get("date")
                content = get_mail_response.get("htmlBody")

                if (sender == "confirm@joompers.com" and subject == "Account delete process"):
                    pattern_to_look_for = re.search(r"Your code: <b>([^<]+)</b>", content)
                    confirmation_code = pattern_to_look_for.group(1) \
                        if (pattern_to_look_for) else None  # returns code found - or None if not found
                    if confirmation_code is not None:
                        date_parsed = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
                        all_codes_with_dates_detected.append((date_parsed, confirmation_code))

            if len(all_codes_with_dates_detected) == 0:  # if no mail with confirmation code was detected
                print(f"No confirmation code to delete user detected in email")

            if len(all_codes_with_dates_detected) > 1:  # if more then one mail with conformation code detected
                code_found = max(all_codes_with_dates_detected, key=lambda x: x[0])[1]  # we select the most recent

            else:  # if only one mail with confirmation code was detected
                code_found = all_codes_with_dates_detected[0][1]

        # print(f"Code found: code_found")
        return code_found

    # deletes the email itself, and also empties instance's variables "email" and "password"
    # used for complete tear-down in test
    def delete_email_generated(self):
        url = "https://www.1secmail.com/mailbox"

        request_data = {
            "action": "deleteMailBox",
            "login": self.email.split('@')[0],
            "domain": self.email.split('@')[1]
        }

        response = requests.post(url, data=request_data)
        assert response.status_code == 200, "Unknown error. Unable to delete the email. Try again"
        print(f"Email {self.email} was deleted\n")
        self.email = None
        self.password = None
