# this class used to:
# - generate temporary email and password needed for user registration
# - checks email and returns confirmation link needed for register user endpoint
# - checks email and returns confirmation code needed for delete user endpoint
# - delete temporary email generated

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

    #  method to randomly create a name for email and password(using lower chars and integers)
    # returns email, password in string data type if email was successfully created;
    # otherwise - returns None for both email and password
    def generate_email_and_password(self):

        #  list of domains used to create an email
        domain_list = [
            "1secmail.com",
            "1secmail.org",
            "1secmail.net"
        ]
        random_domain_from_list = random.choice(domain_list)

        username_symbols = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(username_symbols) for i in
                           range(10))  # by that we create username of 10 random symbols (from lower leters and digits)
        self.email = f'{username}@{random_domain_from_list}'

        password_symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        self.password = ''.join(random.choice(password_symbols) for i in range(
            10))  # by that we create password of 10 random symbols (from lower and upper leters, digits and punctuation)

        print(f"Your email: {self.email}\nYour password: {self.password}")

        #  sending request to log into the email - just to check it works
        log_in_response = requests.get(f"{self.api}?login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}")
        assert log_in_response.status_code == 200, "Unknown error. Unable to log into the email generated. Try again"

        return self.email, self.password

    #  returns one (recent) link if found - or None if not
    def get_link_for_registration(self):
        time.sleep(5)  # time gap to wait for new emails to be received
        link_found = None

        # check the email for mails
        get_mails_response = requests.get(
            f"{self.api}?action=getMessages&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}").json()
        mails_number = len(get_mails_response)

        if mails_number == 0:
            print("No mails in the email detected")

        else:
            list_of_mails_ids = []
            for mail in get_mails_response:
                for key, value in mail.items():
                    if key == "id":  # the "id" key contains value - ID of a specific email
                        list_of_mails_ids.append(
                            value)  # add ID of a specific mail detected into a list of all mail IDs detected in the email itself
            # print(f"The number of mails detected: {mails_number}")


            # finally, getting data from mails
            all_links_with_dates_detected = []

            for mail_id in list_of_mails_ids:
                get_mails_response = requests.get(
                    f"{self.api}?action=readMessage&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}&id={mail_id}").json()  # this response will contain fields such as: "from", "subject", "date", "test_body" and so other
                sender = get_mails_response.get("from")
                subject = get_mails_response.get("subject")
                date = get_mails_response.get("date")
                content = get_mails_response.get("textBody")

                # if (sender == "confirm@joompers.com" and subject == "Welcome to Joompers"): #  TODO

                pattern_to_look_for = re.search("Confirm e-mail\s*<(https?://[^>]+)>", content)
                confirmation_link = pattern_to_look_for.group(1) \
                    if pattern_to_look_for else None  # returns link found or None is not
                if confirmation_link is not None:
                    date_parsed = datetime.strptime(date,
                                                    "%Y-%m-%d %H:%M:%S")  # parsing date into datetime object to be able to iterate on (from the string like that: "Mon, Nov 20, 2023 at 7:56 AM")
                    all_links_with_dates_detected.append((date_parsed, confirmation_link))
                # print(f"Confirmation link found in email: {confirmation_link}")

            if len(all_links_with_dates_detected) == 0:  # if no mail with confirmation link was detected
                print(f"No confirmation link for user registration detected in email")

            if len(all_links_with_dates_detected) > 1:  # if more then one email with conformation link detected
                link_found = max(all_links_with_dates_detected,
                                 key=lambda x: x[0])  # we select most recent mail (and so link)

            else:  # if only one mail with confirmation link was detected
                link_found = all_links_with_dates_detected[0][1]

        # print(f"Link found: {link_found}")
        return link_found

    def get_confirmation_code_for_delete_user(self):
        time.sleep(5)
        code_found = None

        log_in_response = requests.get(f"{self.api}?login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}")

        # check the email for mails
        get_mail_response = requests.get(
            f"{self.api}?action=getMessages&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}").json()
        messages_number = len(get_mail_response)

        if messages_number == 0:
            print("No mails in the email detected")
        else:
            list_of_mails_ids = []
            for mail in get_mail_response:
                for key, value in mail.items():
                    if key == "id":  # the "id" key contains value - ID of a specific email
                        list_of_mails_ids.append(
                            value)  # add ID of a specific mail detected into a list of all mail IDs detected in the email itself
            # print(f"The number of mails detected: {messages_number}")

            # finally, getting data from mails
            all_codes_with_dates_detected = []

            for mail_id in list_of_mails_ids:
                get_mail_response = requests.get(
                    f"{self.api}?action=readMessage&login={self.email.split('@')[0]}&domain={self.email.split('@')[1]}&id={mail_id}").json()  # this response will contain fields such as: "from", "subject", "date", "test_body" and so other
                sender = get_mail_response.get("from")
                subject = get_mail_response.get("subject")
                date = get_mail_response.get("date")
                content = get_mail_response.get("textBody")

                if (sender == "confirm@joompers.com" and subject == "Account delete process"):
                    pattern_to_look_for = re.search(r"Confirm e-mail \*(.*?)\*", content)
                    confirmation_code = pattern_to_look_for.group(1) \
                        if (pattern_to_look_for) else None  # returns code found or None is not
                    if confirmation_code is not None:
                        date_parsed = datetime.strptime(date,
                                                        "%Y-%m-%d %H:%M:%S")  # parsing date into datetime object to be able to iterate on (from the string like that: "Mon, Nov 20, 2023 at 7:56 AM")
                        all_codes_with_dates_detected.append((date_parsed, confirmation_code))
                    # print(f"Confirmation code found in email: {confirmation_code}")

            if len(all_codes_with_dates_detected) == 0:  # if no mail with confirmation code was detected
                print(f"No confirmation code to delete user detected in email")

            if len(all_codes_with_dates_detected) > 1:  # if more then one email with conformation code detected
                link_found = max(all_codes_with_dates_detected,
                                 key=lambda x: x[0])  # we select most recent mail (and so code)

            else:  # if only one mail with confirmation code was detected
                link_found = all_codes_with_dates_detected[0][1]

        return code_found

    #  deletes the email generated before, and also empties instance's "email" and "password" values
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


# # snippet of code for testing the class
#
# generator = EmailAndPasswordGenerator()
# generator.generate_email_and_password()
# # generator.get_link_for_registration()
# generator.get_confirmation_code_for_delete_user()
# generator.delete_email_generated()
