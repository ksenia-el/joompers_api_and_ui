import pytest
import requests
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
import sys

@allure.feature('Get all chat conversations')
@allure.description('Chat conversations with negative limit')
@allure.severity('Normal')

def test_get_all_conversations_with_negative_limit(authenticated_session):
    conversation_api = Conversation(authenticated_session)
    params = {
        'limit': -1,  # Отрицательное значение для limit
        'offset': 0
    }

    response_json, status_code = conversation_api.chat_list(params)

    if status_code == 500: 
        print("Response JSON:", response_json)
        assert True 
    else:
        assert False, f"Unexpected status code: {status_code} - Expected 500 for negative limit"
