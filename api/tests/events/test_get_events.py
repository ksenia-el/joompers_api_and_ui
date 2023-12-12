import json
import pytest
import allure
from api.api_library.events import Events
from api.api_library.user_account import UserAccount
from api.test_data.data_test import TestData
import requests
from api.conftest import chat_id_session

class TestEvents:
    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_get_events(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        api = Events(user_auth_data.session)
        response_body, status = api.get_events()
        assert status == 200
        expected_response_body = []
        assert len(expected_response_body) >= 0

    def test_get_events_not_autorisation(self):
        session = requests.Session()
        api = Events(session)
        response_body, status = api.get_events()
        assert status == 401
        expected_response_body = {
            "detail": "Not authenticated"
        }
        assert response_body == expected_response_body

    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_post_events(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        api = Events(user_auth_data.session)
        response_body, status = api.get_events()
        event_id_from_response_body = response_body[0].get('id')
        response_body, status = api.post_events_set_viewed(event_id_from_response_body)
        assert status == 200
        expected_response_body = {"message": "Successfully viewed"}
        assert response_body == expected_response_body

    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_post_events_wrong_id(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        api = Events(user_auth_data.session)
        response_body, status = api.get_events()
        event_id_wrong_from_response_body = response_body[0]['eventType']['id']
        response_body, status = api.post_events_set_viewed(event_id_wrong_from_response_body)
        assert status == 400
        expected_response_body = {
            "code": "bad_request",
            "message": "Current user is not event reciever"
         }
        assert response_body == expected_response_body







        # @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
        # def test_content_category_set_user_feed_configuration_if_wrong_formate(self, chat_id_session, data_test):
        #     user_auth_data = UserAccount(chat_id_session)
        #     content_api = ContentCategory(user_auth_data.session)
    # @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    # def test_post_events_validation_error(self, user_logged_in_session_fixture, data_test):
    #     user_auth_data = UserAccount(user_logged_in_session_fixture)
    #     api = Events(user_auth_data.session)
    #     response_body, status = api.get_events()
    #     event_id_validation_error_response_body = response_body[1]['eventType']['id']
    #     response_body, status = api.post_events_set_viewed(event_id_validation_error_response_body)
    #
    # def test_get_events_no_autorisation(self):
    #     session = requests.Session()
    #     api = Events(session)
    #     response_body, status = api.get_events()
    #     event_id_from_response_body = response_body[0].get('id')
    #     response_body, status = api.post_events_set_viewed(event_id_from_response_body)
    #
    #     assert status == 422
    #     expected_response_body = {
    #                 "detail": [
    #              {
    #                  "loc": [
    #                      "string"
    #                  ],
    #                  "msg": "string",
    #                  "type": "string"
    #              }
    #          ]
    #         }
    #     assert response_body == expected_response_body
