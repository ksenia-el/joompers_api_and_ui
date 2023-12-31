import requests
import allure


class UserAccount:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    @allure.step('Register user with credentials provided in test data')
    def user_registration(self, username, email, password):
        request_body = {
            "username": username,
            "email": email,
            "password": password
        }

        response = self.session.post(
            self.base_url + "/api/registration",
            json=request_body  # !use this form for each request in JSON format, no "json.dumps()" needed
        )
        status = response.status_code
        return response.json(), status

    def confirm_email(self, token):
        response = self.session.get(
            self.base_url + f"/api/email/confirm_email/{token}"
        )
        return response.json(), response.status_code

    def log_in_with_email(self, email_or_username, password):
        request_body = {
            "username": email_or_username,
            "password": password
        }
        response = self.session.post(
            self.base_url + "/api/login/oauth",
            data=request_body  # !use this form for each request in x-www-form-urlencoded format
        )
        status = response.status_code
        # by "response_data.get()" we can later obtain values from such fields: "user_profile_id",
        # "user_role", "user_status", "access_token"
        return response.json(), status

    def login_via_google(self):
        pass  # TODO

    def user_logout(self):
        response = self.session.post(
            self.base_url + "/api/logout"
        )
        return response.json(), response.status_code

    def request_delete_user(self):
        response = self.session.post(
            self.base_url + "/api/delete/request_delete"
        )
        return response.json(), response.status_code

    def delete_user(self, code):
        response = self.session.delete(
            self.base_url + f"/api/delete/user/{code}"
        )
        return response.json(), response.status_code

    #  TODO:
    def change_user_role(self):
        pass


    def username_check(self, username):
        request_body = {"username": username}
        response = self.session.post(
            self.base_url + "/api/registration/username_check",
            json=request_body
        )
        # TODO: customise return for successful and non- responses
        return response.status_code


    @allure.step('Register user with the custom request_body provided in parameters')
    def user_registration_custom_body(self, request_body):
        response = self.session.post(
            self.base_url + "/api/registration",
            json=request_body
        )
        status = response.status_code
        return response.json(), status

    @allure.step('Log in with the custom request_body provided in parameters')
    def log_in_with_email_custom_body(self, request_body):
        response = self.session.post(
            self.base_url + "/api/login/oauth",
            data=request_body  # !use this form for each request in x-www-form-urlencoded format
        )
        status = response.status_code
        return response.json(), status
