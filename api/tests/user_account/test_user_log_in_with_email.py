import pytest
from api.api_library.user_account import UserAccount
import allure
from api.support.temporary_email_generator import EmailAndPasswordGenerator
from api.conftest import user_not_logged_in_session_fixture
from api.conftest import new_user_logged_in_session_fixture
from api.support.temporary_email_generator import EmailAndPasswordGenerator


class TestUserLogInWithEmail:

    @allure.feature('User log in')
    @allure.description('User logs in with valid credentials')
    @allure.severity('Critical')
    def test_user_log_in_with_email_positive(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)
        response, status = api.log_in_with_email(email, password)
        assert status == 200

        # TODO: add assertion for response_body structure

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture

    def test_user_log_in_with_incorrect_email_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)

        # do some alternations in the email to make it incorrect,
        # here - we just delete the first symbol in it
        altered_email = email[1:]

        response, status = api.log_in_with_email(altered_email, password)
        assert status == 404
        expected_response_body = {
            "code": "not_found_error",
            "message": "User was not found"
        }
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture


    def test_user_log_in_incorrect_password_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)

        # do some alternations in the password to make it incorrect,
        # here - we just delete the first symbol in it
        altered_password = password[1:]

        response, status = api.log_in_with_email(email, altered_password)
        assert status == 400
        expected_response_body = {
            "code": "auth_error",
            "message": "Incorrect password"
        }
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture

    def test_user_log_in_not_exist_negative(self, user_not_logged_in_session_fixture):
        # just generate email and password (without user registration)
        email_and_password_generator = EmailAndPasswordGenerator()
        username, email, password = email_and_password_generator.generate_username_and_email_and_password()

        unauthorized_session = user_not_logged_in_session_fixture
        api = UserAccount(user_not_logged_in_session_fixture)

        response, status = api.log_in_with_email(email, password)
        assert status == 404
        expected_response_body = {
            "code": "not_found_error",
            "message": "User was not found"
        }
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture


    def test_user_log_in_no_email_field_and_its_value_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        api = UserAccount(user_not_logged_in_session_fixture)
        request_body = {
            "password": password

        }
        response, status = api.log_in_with_email_custom_body(request_body)

        expected_response_body = {'detail':
                                      [{'loc': ['body', 'username'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'}]
                                  }
        assert status == 422
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture


    def test_user_log_in_no_password_field_and_its_value_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        api = UserAccount(user_not_logged_in_session_fixture)
        request_body = {
            "username": email
        }
        response, status = api.log_in_with_email_custom_body(request_body)

        expected_response_body = {'detail':
                                      [{'loc': ['body', 'password'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'}]
                                  }
        assert status == 422
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture


    def test_user_log_in_empty_value_in_email_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)
        request_body = {"username": "",
                        "password": password
        }
        response, status = api.log_in_with_email_custom_body(request_body)

        expected_response_body = {'detail':
                                      [{'loc': ['body', 'username'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'}]
                                  }
        assert status == 422
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture

    def test_user_log_in_empty_value_in_password_negative(self, new_user_logged_in_session_fixture, user_not_logged_in_session_fixture):
        # precondition: to have a user account already created (done by new_user_logged_in_session_fixture)
        email = new_user_logged_in_session_fixture[1]
        password = new_user_logged_in_session_fixture[2]

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)
        request_body = {"username": email,
                        "password": ""
                        }
        response, status = api.log_in_with_email_custom_body(request_body)
        expected_response_body = {'detail':
                                      [{'loc': ['body', 'password'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'}]
                                  }
        assert status == 422
        assert response == expected_response_body

        # now the user account and the email created before will be
        # automatically deleted by the new_user_logged_in_session_fixture


    def test_user_log_in_empty_request_body_negative(self, user_not_logged_in_session_fixture):
        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)

        empty_request_body = {}
        response, status = api.log_in_with_email_custom_body(empty_request_body)
        expected_response_body = {'detail':
                                      [{'loc': ['body', 'username'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'},
                                       {'loc': ['body', 'password'],
                                        'msg': 'field required',
                                        'type': 'value_error.missing'}]
                                  }
        assert status == 422
        assert response == expected_response_body





