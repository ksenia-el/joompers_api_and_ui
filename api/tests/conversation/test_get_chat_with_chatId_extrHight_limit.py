import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with extremely limit')
@allure.severity('Normal')
@pytest.mark.parametrize("limit, offset, expected_status", [
    (9999999, 0, 200)
])

def test_get_chat_with_chatId_extremely_hight_limit(authenticated_session, chat_id, limit, offset, expected_status):
   
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list_with_chatId(chat_id, limit, offset)

    expected_response = TestData.get_expected_response()[1]

    assert status_code == expected_status