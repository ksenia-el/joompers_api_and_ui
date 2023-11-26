import pytest
import requests
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation


def test_get_all_conversations_with_custom_limit_and_offset(authenticated_session):
    conversation_api = Conversation(authenticated_session)
    params = {
        'limit': 50,
        'offset': 1
    }

    response_json, status_code = conversation_api.chat_list(params)

    print("Status Code:", status_code)
    print("Response JSON:", response_json)

    expected_response = TestData.get_expected_response()

    assert status_code == 200

    assert len(response_json) <= 50, "The number of chats exceeds the limit"

    for expected_item, response_item in zip(expected_response, response_json):
        check_structure(expected_item, response_item)

def check_structure(expected, actual):
    if isinstance(expected, dict):
        for key, expected_type in expected.items():
            if key in actual:
                actual_value = actual[key]

                # Позволяем None для определенных полей
                if actual_value is None and key in ['photoUrl', 'unreadCount']:
                    continue  # Пропускаем проверку типа, если значение None и это допустимо

                # Проверяем тип, если ключ присутствует
                if isinstance(expected_type, type):
                    assert isinstance(actual_value, expected_type), f"Type of {key} is not {expected_type.__name__}"
                else:
                    check_structure(expected_type, actual_value)
            else:
                # Обработка отсутствия необязательных ключей
                print(f"Optional key {key} is missing in response")
    elif isinstance(expected, list):
        for expected_elem, actual_elem in zip(expected, actual):
            check_structure(expected_elem, actual_elem)

