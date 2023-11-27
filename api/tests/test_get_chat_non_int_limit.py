import pytest
import requests
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
import sys

@allure.feature('Get all chat conversations')
@allure.description('Chat conversations with non integer limit')
@allure.severity('Normal')
@pytest.mark.parametrize("params, expected_status", [
    ({"limit": 'one', "offset": 0}, 422),

])

def test_get_all_conversations_with_non_integer_limit(authenticated_session, params, expected_status):
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list(params)

    expected_response = TestData.get_expected_response()

    assert status_code == expected_status
