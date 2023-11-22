import pytest
from api_library import Endpoints
from test_data import TestData
from conftest import user_logged_in_session_fixture
import allure


class TestDeleteUser:

    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_delete_user_positive(self, user_logged_in_session_fixture, test_data):
        api = Endpoints(user_logged_in_session_fixture)
        # TODO: how to get confirmation code from email?
        response_body, status = api.delete_user("-fSr9po4")  # TODO
        message = response_body.get("message")
        assert status == 200
        assert message == "Successfully deleted"
