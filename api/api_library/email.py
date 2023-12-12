import requests

class   Email:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    def email_subscription(self):
        response = self.session.post(
            self.base_url + "/api/email/subscription",
        )
        status = response.status_code
        return response.json(), status

    def email_cancel_subscription(self):
        response = requests.post(
            self.base_url + "/api/email/subscription",
        )
        status = response.status_code
        return response.json(), status