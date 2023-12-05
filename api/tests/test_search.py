import pytest
import allure
from api.api_library.search import Search
import requests
from api.conftest import user_logged_in_session_fixture

class TestSearch:

        def test_search(self):
            session = requests.Session()
            api = Search(session)
            params = {
                'limit': 100,
                'offset': 0,
                'searchString':''
            }
            response_body, status = api.search_user(params)
            assert status == 200
            expected_response_body = {
                "searchProfile": [],
                "searchHashtags": []
            }
            assert len(expected_response_body) >= 0

        # def test_get_search_not_autorisation(self):
        #     session = requests.Session()
        #     api = Search(session)
        #
        #     response_body, status = api.search_user()
        #     assert status == 422
        #     expected_response_body = {
        #         "detail": "Not authenticated"
        #     }
        #     assert response_body == expected_response_body
