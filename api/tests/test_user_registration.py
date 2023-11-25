import pytest
import allure
from api.api_library.user_account import UserAccount
from api.test_data.test_data_user_account import TestData
import requests


class TestUserRegistration:


    @allure.feature('User registration')
    @allure.description('Register user with valid credentials')
    @allure.severity('Critical')
    @pytest.mark.parametrize("credentials", TestData.valid_user_credentials)
    def test_user_registration_positive(self, credentials):
        session = requests.Session()
        api = UserAccount(session)
        response_body, status = api.user_registration(credentials)
        assert status == 201
        #  TODO: how to get a link to confirm registration from email?
        expected_response_body = {
          "message": "successful"
        }
        assert response_body == expected_response_body

    @pytest.mark.parametrize("credentials", TestData.valid_user_credentials)
    def test_user_registration_second_attempt_negative(self, credentials):
        session = requests.Session()
        api = UserAccount(session)
        response_body, status = api.user_registration(credentials)
        assert status == 400
        expected_response_body = {
            "code": "already_exist",
            "message": "User with this email is already exist"
        }
        assert response_body == expected_response_body


    def test_user_registration_empty_request_negative(self):
        session = requests.Session()
        api = UserAccount(session)
        request_body = {}
        response_body, status = api.user_registration(request_body)
        assert status == 422
        expected_response_body = {
            "detail": [
                {
                    "loc": [
                        "body",
                        "email"
                    ],
                    "msg": "field required",
                    "type": "value_error.missing"
                },
                {
                    "loc": [
                        "body",
                        "password"
                    ],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }
        assert response_body == expected_response_body

    #  TODO
    def test_user_registration_no_email_provided_negative(self):
        pass

    #  TODO
    def test_user_registration_no_password_provided_negative(self):
        pass

    #  TODO
    def test_user_registration_empty_email_negative(self):
        pass

    #  TODO
    def test_user_registration_empty_password_negative(self):
        pass

    #  TODO
    def test_user_registration_incorrect_value_format_in_email_negative(self):
        pass

    #  TODO
    def test_user_registration_incorrect_value_format_in_password_negative(self):
        pass
