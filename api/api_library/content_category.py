import requests
import allure

class ContentCategory:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    def get_content_category_not_value(self):
        response = requests.get(self.base_url + "/api/content_category/get_content_categories")
        status = response.status_code
        return response.json(), status

    def get_content_category_landing_true(self):
        response = requests.get(self.base_url + "/api/content_category/get_content_categories?is_landing_show=true")
        status = response.status_code
        return response.json(), status


    def get_content_category_landing_false(self):
        response = requests.get(self.base_url + "/api/content_category/get_content_categories?is_landing_show=false")
        status = response.status_code
        return response.json(), status


    def content_category_set_user_feed_configuration(self, id):
        response = self.session.post(
            self.base_url + "/api/content_category/set_user_feed_configuration",
            json={"content_category_ids": [id]}
        )
        status = response.status_code
        return response.json(), status
