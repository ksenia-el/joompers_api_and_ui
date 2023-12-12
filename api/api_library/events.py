import requests

class Events:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    def get_events(self):
        response = self.session.get(
            self.base_url + "/api/events/")
        status = response.status_code
        return response.json(), status

    def post_events_set_viewed(self, viewed_id):
        response = self.session.post(
            self.base_url + f'/api/events/set_viewed/{viewed_id}'
        )
        status = response.status_code
        return response.json(), status


