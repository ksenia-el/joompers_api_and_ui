import json
import pytest
import allure
from api.api_library.email import Email
from api.api_library.user_account import UserAccount
from api.test_data.data_test import TestData
import requests
from api.conftest import chat_id_session

class TestEmail:
    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_email_subscription(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        api = Email(user_auth_data.session)
        response_body, status = api.email_subscription()
        assert status == 200
        expected_response_body = {"message": "Successfully turned on subscription"
    }
        assert response_body == expected_response_body


    def test_email_subscription_not_autorisation(self):
        session = requests.Session()
        api = Email(session)
        response_body, status = api.email_subscription()
        assert status == 401
        expected_response_body = {"detail": "Not authenticated"}
        assert response_body == expected_response_body