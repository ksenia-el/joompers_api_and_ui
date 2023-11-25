import pytest
from api.api_library.user_account import UserAccount
from api.test_data.test_data_register_and_login_and_logout_and_delete_user import TestData
from api.conftest import user_logged_in_session_fixture


class TestDeleteUser:

    @pytest.mark.parametrize("test_data", TestData.valid_user_credentials)
    def test_delete_user_positive(self, user_logged_in_session_fixture, test_data):
        api = UserAccount(user_logged_in_session_fixture)
        # TODO: how to get confirmation code from email?
        response_body, status = api.delete_user("-fSr9po4")  # TODO
        message = response_body.get("message")
        assert status == 200
        assert message == "Successfully deleted"
