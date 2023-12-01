import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
from api.conftest import user_logged_in_session_fixture

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with extremely limit')
@allure.severity('Normal')
@pytest.mark.parametrize("limit, offset, expected_status", [
    (9999999, 0, 200)
])

def test_get_chat_with_chatId_extremely_hight_limit(user_logged_in_session_fixture, chat_id, limit, offset, expected_status):
    authenticated_session = user_logged_in_session_fixture[0]
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list_with_chatId(chat_id, limit, offset)

    expected_response = TestData.get_expected_response()[1]

    assert status_code == expected_status