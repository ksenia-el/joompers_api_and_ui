import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with negative limit')
@allure.severity('Normal')
def test_get_chat_with_chatId_negative_limit(authenticated_session):
    conversation_api = Conversation(authenticated_session)
    chat_id = '68eda51b-a945-40ee-bbaa-dc1daa79ad06'
    response_json, status_code = conversation_api.chat_list_with_chatId(chat_id, -1, 0)

    expected_response = TestData.get_expected_response()[1]

    if status_code == 500: 
        print("Response JSON:", response_json)
        assert True 
    else:
        assert False, f"Unexpected status code: {status_code} - Expected 500 for negative limit"
