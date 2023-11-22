import pytest
from api_library import Endpoints
from test_data import TestData
from conftest import user_logged_in_session_fixture
import allure


class TestUserLogOut:

    @allure.feature('User log out')
    @allure.description('User authenticated logs out')
    @allure.severity('Critical')
    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_user_log_out_positive(self, user_logged_in_session_fixture, test_data):
        api = Endpoints(user_logged_in_session_fixture)  # create an Endpoints instance using this type of session created by a specific fixture (used for requests that needs Authorization)
        response_body, status = api.user_logout()
        message = response_body.get("message")
        assert status == 200
        assert message == "You have been logout"

