import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with non integer limit and offset')
@allure.severity('Normal')
@pytest.mark.parametrize("limit, offset, expected_status", [
    ('one', 0, 422),
    (100, 'one', 422)
])

def test_get_chat_with_chatId_non_integer_limit_and_offset(authenticated_session, chat_id, limit, offset, expected_status):
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list_with_chatId(chat_id, limit, offset)

    expected_response = TestData.get_expected_response()[1]

    assert status_code == expected_status
