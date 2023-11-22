import requests
import allure


class Endpoints:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session


    @allure.step('Register user with credentials provided in test data')
    def user_registration(self, request_body):
        response = requests.post(
            self.base_url + "/api/registration",
            json=request_body  # !use this form for each request in JSON format, no "json.dumps()" needed
        )
        status = response.status_code
        return response.json(), status


    def log_in_with_email(self, email_or_username, password):
        request_body = {
            "username": email_or_username,
            "password": password
        }
        response = requests.post(
            self.base_url + "/api/login/oauth",
            data=request_body  # !use this form for each request in x-www-form-urlencoded format
        )
        status = response.status_code
        # user_profile_id = response_data.get("user_profile_id")
        # user_role = response_data.get("user_role")
        # user_status = response_data.get("user_status")
        # access_token = response_data.get("access_token")
        return response.json(), status

    def user_logout(self):
        response = self.session.post(
            self.base_url + "/api/logout"
        )
        # message = response_data.get("message")
        return response.json(), response.status_code

    def request_delete_user(self):
        response = self.session.post(
            self.base_url + "/api/delete/request_delete"
        )
        # message = response_data.get("message")
        return response.json(), response.status_code

    def delete_user(self, code):
        response = self.session.delete(
            self.base_url + f"/api/delete/user/{code}"
        )
        # message = response.json().get("message")
        return response.json(), response.status_code

