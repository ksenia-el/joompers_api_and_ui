import pytest
import requests
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
import sys
from api.conftest import user_logged_in_session_fixture

@allure.feature('Get all chat conversations')
@allure.description('Chat conversations with high limit')
@allure.severity('Normal')
@pytest.mark.parametrize("params, expected_status", [
    ({"limit": 9999999, "offset": 0}, 200),
])

def test_get_all_conversations_with_extremely_high_limit(user_logged_in_session_fixture, params, expected_status):
    authenticated_session = user_logged_in_session_fixture[0]
    conversation_api = Conversation(authenticated_session)
    
    response_json, status_code = conversation_api.chat_list(params)

    expected_response = TestData.get_expected_response()

    assert status_code == expected_status
