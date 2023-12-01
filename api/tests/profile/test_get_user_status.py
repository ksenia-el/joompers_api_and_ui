import allure
import pytest

from api.api_library.profile import Profile
from api.conftest import user_logged_in_session_fixture


class TestGetUserStatus:
    @allure.feature("Get user current status")
    @allure.severity('Major')
    def test_get_user_status_success(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)

        response_body, status = profile_api.get_user_status()
        assert status == 200
        assert response_body == "active"

    # def test_get_user_status_unauthenticated(self, user_logged_in_session_fixture):
    #     authenticated_session = user_logged_in_session_fixture[0]
    #     profile_api = Profile(authenticated_session)
    #
    #     response_body, status = profile_api.get_user_status()
    #     assert status == 422


