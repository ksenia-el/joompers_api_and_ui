import pytest
import requests
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
import sys

@allure.feature('Get all chat conversations')
@allure.description('Chat conversations with negative offset')
@allure.severity('Normal')
@pytest.mark.parametrize("params, expected_status", [
    ({"limit": 100, "offset": -1}, 500),

])

def test_get_all_conversations_with_negative_offset(authenticated_session, params, expected_status):
    conversation_api = Conversation(authenticated_session)
  
    response_json, status_code = conversation_api.chat_list(params)

    if status_code == expected_status: 
        print("Response JSON:", response_json)
        assert True 
    else:
        assert False, f"Unexpected status code: {status_code} - Expected 500 for negative offset"

