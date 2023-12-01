import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema


# @allure.feature("Get user followers list")
# @allure.severity('Major')
class TestGetUserFollowings:
    def test_get_profile_for_role_creator_my_own_account(self, authenticated_session, uuid_retrieval):
        profile_api = Profile(authenticated_session)
        uuid = uuid_retrieval
        response_body, status_code = profile_api.get_user_profile(uuid)
        assert status_code == 200, "Failed to get user profile"
        try:
            validate(instance=response_body, schema=schema.get_profile_creator_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_profile_for_role_creator_max_account(self, authenticated_session):
        profile_api = Profile(authenticated_session)
        uuid = "500e8112-e2fb-446b-9de2-251cf491708d"
        response_body, status_code = profile_api.get_user_profile(uuid)
        assert status_code == 200, "Failed to get user profile"
        try:
            validate(instance=response_body, schema=schema.get_profile_creator_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_profile_for_role_user(self, authenticated_session, uuid_retrieval):
        profile_api = Profile(authenticated_session)
        uuid = "aae58dd2-c9b9-4f7b-b653-3eedc97b5a09"
        response_body, status_code = profile_api.get_user_profile(uuid)
        assert status_code == 200, "Failed to get user followings"
        print(response_body)
        try:
            validate(instance=response_body, schema=schema.get_profile_user_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
    #
    # def test_get_user_profile_with_non_existing_user_profile_id(self, authenticated_session, uuid_retrieval):
    #     profile_api = Profile(authenticated_session)
    #     uuid = "9fa85f64-5717-4562-b3fc-2c963f66afa6"
    #     response_body, status_code = profile_api.get_profile_followings(uuid)
    #
    #     assert status_code == 404, f"Expected 404 for non existing user_profile_id, got {status_code} instead"
    #     try:
    #         validate(instance=response_body, schema=schema.get_followers_response_schema_not_found_error())
    #     except jsonschema.exceptions.ValidationError as e:
    #         assert False, f"Response did not match schema: {e}"
    #
    # def test_get_user_profile_with_invalid_format_user_profile_id(self, authenticated_session, uuid_retrieval):
    #     profile_api = Profile(authenticated_session)
    #     uuid = "abc"
    #     response_body, status_code = profile_api.get_profile_followings(uuid)
    #     assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
    #     try:
    #         validate(instance=response_body, schema=schema.get_followers_response_schema_validation_error())
    #     except jsonschema.exceptions.ValidationError as e:
    #         assert False, f"Response did not match schema: {e}"