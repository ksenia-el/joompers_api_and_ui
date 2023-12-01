import pytest
from api.api_library.user_account import UserAccount
from api.test_data.test_data_user_account import TestData
import requests
import allure
from api.support.temporary_email_generator import EmailAndPasswordGenerator
from api.conftest import user_not_logged_in_session_fixture


class TestUserLogInWithEmail:

    @allure.feature('User log in')
    @allure.description('User logs in with valid credentials')
    @allure.severity('Critical')
    def test_user_log_in_with_email_positive(self, user_not_logged_in_session_fixture):
        email_and_password_generator = EmailAndPasswordGenerator()
        email, password = email_and_password_generator.generate_email_and_password()

        not_authorized_session = user_not_logged_in_session_fixture
        api = UserAccount(not_authorized_session)  # and create an Endpoints instance from it to run API calls
        response, status = api.log_in_with_email(email, password)
        assert status == 200



