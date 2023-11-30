import pytest
import allure
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Send message with chatId')
@allure.description('Send message to chat by chatId')
@allure.severity('Normal')
@pytest.mark.parametrize("message, expected_status", [
    ("Test message 1", 201),
    ("!№;%:?*+.,-)(}{", 201),
    ("", 201)
])
def test_send_message_with_chatId(authenticated_session, chat_id, message, expected_status):
    conversation_api = Conversation(authenticated_session)
    
    response_json, status_code = conversation_api.chat_with_chatId_post_message(chat_id, message)

    print("Status Code:", status_code)
    print("Response JSON:", response_json)

    assert status_code == expected_status, f"Expected status code {expected_status}, got {status_code}"

    expected_response = TestData.get_expected_response()[2]  
    for expected_item, response_item in zip(expected_response, response_json):
        check_structure(expected_item, response_item)

def check_structure(expected, actual):
    if isinstance(expected, str):
        assert expected in actual, f"Key '{expected}' is missing in the response"
    elif isinstance(expected, dict):
        for key, expected_value in expected.items():
            assert key in actual, f"Key '{key}' is missing in the response"
            actual_value = actual[key]
            assert actual_value == expected_value, f"Value for '{key}' did not match. Expected: {expected_value}, Got: {actual_value}"
    else:
        raise TypeError("Expected response structure should be a dictionary or a string")



    

