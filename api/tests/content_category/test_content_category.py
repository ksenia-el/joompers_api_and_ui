import jsonschema
import pytest
import allure
from api.api_library.content_category import ContentCategory
from api.api_library.user_account import UserAccount
from api.test_data.data_test import TestData
import requests
from api.conftest import user_logged_in_session_fixture, chat_id_session
import uuid


class TestContentCategory:

    def test_get_content_category_landing_empty_resp_body_has_items(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        assert len(response_body) > 0

    def test_get_content_category_landing_empty_resp_body_is_list(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        assert isinstance(response_body, list)

    def test_get_content_category_landing_empty_resp_body_item_is_dict(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        for item in response_body:
            assert isinstance(item, dict)

    def test_get_content_category_landing_empty_check_each_item_has_id_and_title_keys(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        for item in response_body:
            assert set(item.keys()) == {'id', 'title'}


    def test_get_content_category_landing_empty_check_each_item_has_id_and_title_values_are_strings(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        for item in response_body:
            assert isinstance(item['id'], str)
            try:
                uuid.UUID(item['id'], version=4)
            except ValueError:
                assert False, "ID is not in the format of UUID"
            assert isinstance(item['title'], str)


    def test_get_content_category_landing_empty_resp_body_is_expected_type_and_length(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        assert status == 200
        expected_response_body = [
            {
                 "id": "b9a1171e-9228-46c2-914b-2d14928de2c0",
                "title": "All"
             },
             {
                 "id": "92cab661-f750-49cf-9a14-3996841a8179",
                 "title": "Articles"
            },
            {
                "id": "a37eb0fb-2e32-4b71-af2d-c84f0fd204a9",
                 "title": "Books"
             },
             {
                 "id": "9241308b-9a01-4444-b752-4c6229c5f97f",
                 "title": "E-books"
             },
             {
                 "id": "f3645178-9b39-45cd-99c7-0d8b9a2eefb4",
                 "title": "Illustrations"
             },
             {
                "id": "8088910e-a505-4a2e-a2eb-73d55c2b5926",
                "title": "Interviews"
            },
             {
                "id": "fba72428-aaba-48ba-86ae-9ae2ced13e5e",
                 "title": "Music"
            },
             {
                 "id": "8f9ae04b-c0a8-4f6b-856e-865a23683a16",
                 "title": "Pictures"
            },
             {
                "id": "aca7c1e9-8bf0-4233-a9ee-dc040f34f2b6",
                "title": "Podcasts"
            },
             {
                 "id": "b3b64d90-0aed-4279-8a2c-e41bb077476a",
                 "title": "Sound footages"
             },
            {
                "id": "94eaf203-bcb9-417e-93f6-6bc222843b8a",
                "title": "Study"
            },
             {
                 "id": "336c9ffb-b2dd-45c9-9fe4-1edb278bc96d",
                 "title": "Video"
            },
             {
                 "id": "8b5e0d9a-d1c3-4f4d-8d46-e29d7586fc36",
                 "title": "Vlogs"
             }
         ]
        count_items_response_body = 13
        assert count_items_response_body == len(expected_response_body)
        assert response_body == expected_response_body
        assert type(response_body) == type(expected_response_body)


    def test_get_content_category_landing_true_resp_body_is_expected_type_and_length(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_landing_true()
        assert status == 200
        count_items_expected_response_body = 9
        expected_response_body = []
        assert count_items_expected_response_body == len(response_body)
        assert type(response_body) == type(expected_response_body)

    def test_get_content_category_landing_false_resp_body_is_expected_type_and_length(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_landing_false()
        assert status == 200
        count_items_expected_response_body = 13
        expected_response_body = []
        assert count_items_expected_response_body == len(response_body)
        assert type(response_body) == type(expected_response_body)

    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_content_category_set_user_feed_configuration(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        content_api = ContentCategory(user_auth_data.session)
        response_body, status = content_api.get_content_category_not_value()
        request_body = response_body[0].get('id')
        response_body, status = content_api.content_category_set_user_feed_configuration(request_body)
        assert status == 201
        expected_response_body = {"message": "Your feed was successfully set"}
        assert response_body == expected_response_body


    def test_content_category_set_user_feed_configuration_if_not_authorization(self):
        session = requests.Session()
        api = ContentCategory(session)
        response_body, status = api.get_content_category_not_value()
        request_body = response_body[0].get('id')
        response_body, status = api.content_category_set_user_feed_configuration(request_body)
        assert status == 401
        expected_response_body = {"detail": "Not authenticated"}
        assert response_body == expected_response_body


    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_content_category_set_user_feed_configuration_if_wrong_formate(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        content_api = ContentCategory(user_auth_data.session)
        response_body, status = content_api.content_category_set_user_feed_configuration('test')
        assert status == 422
        expected_response_body = {
                "detail": [
        {
                "loc": [
                "body",
                "content_category_ids",
                0
              ],
                 "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
                }
            ]
        }
        assert response_body == expected_response_body

    @pytest.mark.parametrize("data_test", TestData.valid_user_credentials)
    def test_content_category_set_user_feed_configuration_if_wrong_formate(self, chat_id_session, data_test):
        user_auth_data = UserAccount(chat_id_session)
        content_api = ContentCategory(user_auth_data.session)
        response_body, status = content_api.content_category_set_user_feed_configuration('123f')
        assert status == 422
        expected_response_body = {
            "detail": [
                {
                    "loc": [
                        "body",
                        "content_category_ids",
                        0
                    ],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid"
                }
            ]
        }
        assert response_body == expected_response_body




# user_data = user_api.log_in_with_email(data_test['email'], data_test['password'])
        # access_token = user_data[0]['access_token']
        # session = requests.Session()
        # session.headers.update({"Authorization": f"Bearer {access_token}"})