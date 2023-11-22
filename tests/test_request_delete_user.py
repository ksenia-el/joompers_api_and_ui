import allure
import pytest
from api_library import Endpoints
from test_data import TestData
from conftest import user_logged_in_session_fixture
import allure


class TestRequestDeleteUser:

    @allure.feature('Request delete user')
    @allure.description('Request deletion of existing user account')
    @allure.severity('Critical')
    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_request_delete_user_positive(self, user_logged_in_session_fixture, test_data):
        api = Endpoints(user_logged_in_session_fixture)
        response_body, status = api.request_delete_user()
        message = response_body.get("message")
        expected_message = "Message has been sent for your email"
        assert status == 200
        assert message == expected_message
