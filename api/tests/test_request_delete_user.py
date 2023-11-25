import pytest
from api.api_library.user_account import UserAccount
from api.test_data.test_data_register_and_login_and_logout_and_delete_user import TestData
from api.conftest import user_logged_in_session_fixture
import allure


class TestRequestDeleteUser:

    @allure.feature('Request delete user')
    @allure.description('Request deletion of existing user account')
    @allure.severity('Critical')
    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_request_delete_user_positive(self, user_logged_in_session_fixture, test_data):
        api = UserAccount(user_logged_in_session_fixture)
        response_body, status = api.request_delete_user()
        message = response_body.get("message")
        expected_message = "Message has been sent for your email"
        assert status == 200
        assert message == expected_message
