import requests

class Search:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session


    def search_user(self, params):
        response = requests.get(
            self.base_url + "/api/search",
            params=params)
        status = response.status_code
        return response.json(), status

    # def search_user(self):
    #     response = requests.get(
    #         self.base_url + "/api/search",
    #     )
    #     status = response.status_code
    #     return response.json(), status

