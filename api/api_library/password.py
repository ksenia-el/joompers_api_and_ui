import requests
import allure

# TODO: not tested yet!
# TODO: add description and marks

class Password:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    # change password while being authorized and being in the user profile
    def change_password_in_profile(self, old_password, new_password):
        request_body = {
            "newPassword1": new_password,
            "newPassword2": new_password,
            "oldPassword": old_password
        }

        response = self.session.post(
            self.base_url + "/api/password/change_password_in_profile",
            json=request_body  # !use this form for each request in JSON format, no "json.dumps()" needed
        )
        status = response.status_code
        return response.json(), status

    # the next 3 methods are used for 3-steps process to reset a new password instead of the old that was forgotten
    def request_password_recovery_by_email_or_username(self, email_or_username):
        request_body = {
            "recoveryField": email_or_username
        }

        response = requests.post(
            self.base_url + "/api/password/request_password_recovery",
            json=request_body
        )
        status = response.status_code
        return response.json(), status

    def confirm_password_recovery(self, reset_token):
        response = requests.get(
            self.base_url + f"/api/password/reset_password?reset_token={reset_token}"
        )
        status = response.status_code
        return response.json(), status


    def reset_password(self, new_password, reset_token):
        request_body = {
            "newPassword1": new_password,
            "newPassword2": new_password,
            "resetToken": reset_token
        }
        response = requests.post(
            self.base_url + "/api/password/reset_password",
            json=request_body
        )
        status = response.status_code
        return response.json(), status


    #  ------ NEXT METHODS ARE USED IN NEGATIVE TESTS (to run API-calls with custom request body if needed)

    # change password while being authorized and being in the user profile
    def change_password_in_profile_custom_body(self, request_body):
        response = self.session.post(
            self.base_url + "/api/password/change_password_in_profile",
            json=request_body  # !use this form for each request in JSON format, no "json.dumps()" needed
        )
        status = response.status_code
        return response.json(), status