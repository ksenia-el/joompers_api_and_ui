import requests
import allure

class ContentCategory:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    def content_category(self, request_body):
        response = requests.get(
            self.base_url + "/api/content_category/get_content_categories",
            json=request_body  # !use this form for each request in JSON format, no "json.dumps()" needed
        )
        status = response.status_code
        return response.json(), status

    def content_category_set_user_feed_configuration(self, request_body):
        response = self.session.post(
            self.base_url + "/api/content_category/set_user_feed_configuration",
            json=request_body
        )
        status = response.status_code
        return response.json(), status