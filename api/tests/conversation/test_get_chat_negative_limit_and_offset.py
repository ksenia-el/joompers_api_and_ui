import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
from api.conftest import user_logged_in_session_fixture

@allure.feature('Get chat with chatId')
@allure.description('Chat conversations by chatId with negative limit and offset')
@allure.severity('Normal')
@pytest.mark.parametrize("params, expected_status", [
     ({"limit": -1, "offset": 0}, 500),
      ({"limit": 100, "offset": -1}, 500),
])
def test_get_chat_with_chatId_negative_limit_and_offset(user_logged_in_session_fixture, params, expected_status):
    authenticated_session = user_logged_in_session_fixture[0]
    conversation_api = Conversation(authenticated_session)

    response_json, status_code = conversation_api.chat_list(params)


    if status_code == expected_status: 
        print("Response JSON:", response_json)
        assert True
    else:
        assert False, f"Unexpected status code: {status_code} - Expected {expected_status}"

