
import pytest
from api.api_library.password import Password
from api.support.temporary_email_generator import EmailAndPasswordGenerator
import allure
import api.conftest


class TestUserLogInWithEmail:

    def test_user_log_in_with_email_positive(self, user_logged_in_session_fixture):
        api = Password(user_logged_in_session_fixture)


        response, status = api.log_in_with_email(test_data["email"], test_data["password"])
        assert status == 200
