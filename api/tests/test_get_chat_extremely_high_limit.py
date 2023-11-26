import pytest
import requests
from api.test_data.test_data_conversation import TestData
from api.api_library.conversation import Conversation
import sys



def test_get_all_conversations_with_extremely_high_limit(authenticated_session):
    conversation_api = Conversation(authenticated_session)
    
    params = {
        'limit': 9999999, 
        'offset': 0
    }

    response_json, status_code = conversation_api.chat_list(params)

    expected_response = TestData.get_expected_response()

    assert status_code == 200
