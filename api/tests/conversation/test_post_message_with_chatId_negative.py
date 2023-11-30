import pytest
import allure
import uuid
import json
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation

@allure.feature('Send message with chatId')
@allure.description('Send message to chat by chatId with negative data')
@allure.severity('Normal')
@pytest.mark.parametrize("chat_id, message, expected_status", [
    (str(uuid.uuid4()), "Test message 1", 400),
    (str(uuid.uuid4()), "!№;%:?*+.,-)(}{", 400),
    (str(uuid.uuid4()), "", 400),
    ("", "Test message", 404) 
])
def test_send_message_with_chatId(authenticated_session, chat_id, message, expected_status):
  
    conversation_api = Conversation(authenticated_session)
    
    response_json, status_code = conversation_api.chat_with_chatId_post_message(chat_id, message)

    print("Status Code:", status_code)
    print("Response JSON:", response_json)
    print("Chat ID:", chat_id)

    if status_code == 404:
        expected_response = {
            "detail": "Not Found"
        }
        check_structure(expected_response, response_json)
    elif status_code == 400:
        expected_response = TestData.get_expected_response()[3]  
        check_structure(expected_response, response_json)
    else:
        assert False, f"Unexpected status code {status_code}"

    assert status_code == expected_status, f"Expected status code {expected_status}, got {status_code}"

def check_structure(expected, actual):
    assert isinstance(actual, dict), "Actual response should be a dictionary"

    if 'error' in actual and isinstance(actual['error'], str):
        try:
            actual_error = json.loads(actual['error'])
        except json.JSONDecodeError:
            raise ValueError("Error response is not a valid JSON")

        for key, expected_value in expected.items():
            assert key in actual_error, f"Key '{key}' is missing in the response"
            actual_value = actual_error[key]
            assert actual_value == expected_value, f"Value for '{key}' did not match. Expected: {expected_value}, Got: {actual_value}"
    else:
        for key, expected_value in expected.items():
            assert key in actual, f"Key '{key}' is missing in the response"
            actual_value = actual[key]
            assert actual_value == expected_value, f"Value for '{key}' did not match. Expected: {expected_value}, Got: {actual_value}"


   
