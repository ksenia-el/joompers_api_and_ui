import pytest
import requests
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
from api.conftest import user_logged_in_session_fixture
import sys

@allure.feature('Get all chat conversations')
@allure.description('Chat conversations with non integer limit and offset')
@allure.severity('Normal')
@pytest.mark.parametrize("params, expected_status", [
    ({"limit": 'one', "offset": 0}, 422),
    ({"limit": 100, "offset": 'one'}, 422),
])

def test_get_all_conversations_with_non_integer_limit_and_offset(user_logged_in_session_fixture, params, expected_status):
    authenticated_session = user_logged_in_session_fixture[0]
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list(params)

    expected_response = TestData.get_expected_response()

    assert status_code == expected_status
