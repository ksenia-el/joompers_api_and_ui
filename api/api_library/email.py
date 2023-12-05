import requests

class   Email:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session


    def email_cancel_subscription():
        response = requests.post(
            self.base_url + "/api/email/subscription",
        )
        status = response.status_code
        return response.json(), status