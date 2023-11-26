import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with non integer offset')
@allure.severity('Normal')
def test_get_chat_with_chatId_non_integer_offset(authenticated_session):
    conversation_api = Conversation(authenticated_session)
    chat_id = '68eda51b-a945-40ee-bbaa-dc1daa79ad06'
    response_json, status_code = conversation_api.chat_list_with_chatId(chat_id, 100, 'one')

    expected_response = TestData.get_expected_response()[1]

    assert status_code == 422
