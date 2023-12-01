import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema
from api.conftest import user_logged_in_session_fixture


@allure.feature("Get user followers list")
@allure.severity('Major')
class TestGetUserFollowings:


    def test_get_user_followers_with_valid_user_profile_id(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        uuid = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)

        response_body, status_code = profile_api.get_profile_followings(uuid)
        print(response_body)
        assert status_code == 200, "Failed to get user followings"
        try:
            validate(instance=response_body, schema=schema.get_followings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_user_followings_with_non_existing_user_profile_id(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)

        uuid = "9fa85f64-5717-4562-b3fc-2c963f66afa6"
        response_body, status_code = profile_api.get_profile_followings(uuid)

        assert status_code == 404, f"Expected 404 for non existing user_profile_id, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_not_found_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_user_followings_with_invalid_format_user_profile_id(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)

        uuid = "abc"
        response_body, status_code = profile_api.get_profile_followings(uuid)
        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_validation_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"


