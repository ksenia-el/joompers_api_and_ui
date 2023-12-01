import allure
import pytest

from api.api_library.profile import Profile


class TestGetUserStatus:
    @allure.feature("Get user current status")
    @allure.severity('Major')
    def test_get_user_status_success(self, authenticated_session):
        profile_api = Profile(authenticated_session)
        response_body, status = profile_api.get_user_status()
        assert status == 200
        assert response_body == "active"

    # def test_get_user_status_unauthenticated(self, authenticated_session):
    #     profile_api = Profile(authenticated_session)
    #     response_body, status = profile_api.get_user_status()
    #     assert status == 422


