import pytest
from api_library import Endpoints
from test_data import TestData
import requests
import allure


class TestUserLogInWithEmail:

    @allure.feature('User log in')
    @allure.description('User logs in with valid credentials')
    @allure.severity('Critical')
    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_user_log_in_with_email_positive(self, test_data):
        session = requests.Session()  # create this type of session (used for requests that needs no Authorization)
        api = Endpoints(session)  # and create an Endpoints instance from it to run API calls
        response, status = api.log_in_with_email(test_data["email"], test_data["password"])
        assert status == 200
