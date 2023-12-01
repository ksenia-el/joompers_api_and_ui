import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema


@allure.feature("Get user followers list")
@allure.severity('Major')
class TestGetUserFollowers:

    @pytest.mark.parametrize("user_type", [
        "author",
        "all",
        "user"
    ])
    def test_get_user_followers_with_valid_user_types_and_user_profile_id(self, authenticated_session, uuid_retrieval, user_type):
        profile_api = Profile(authenticated_session)
        uuid = uuid_retrieval
        response_body, status_code = profile_api.get_profile_followers(uuid, user_type)
        assert status_code == 200, "Failed to get user followers"

        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
    @pytest.mark.parametrize("limit, offset", [
        (1, 0),
        (0, 1),
        (3, 1)
    ])
    def test_get_user_followers_limit_and_offset(self, authenticated_session,
                                                 uuid_retrieval, limit, offset):
        profile_api = Profile(authenticated_session)
        uuid = uuid_retrieval
        user_type = "all"
        response_body, status_code = profile_api.get_profile_followers(uuid, user_type, limit=limit, offset=offset)

        assert status_code == 200, "Failed to get user followers"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
        assert len(response_body['profiles']) <= limit, f"Returned more profiles than the limit of {limit}"

    @pytest.mark.parametrize("user_type", [
        "somestring",
        "",
        " ",
        123,
        "^$#>/"
    ])
    def test_get_user_followers_with_invalid_user_type(self, authenticated_session, uuid_retrieval, user_type):
        profile_api = Profile(authenticated_session)
        uuid = uuid_retrieval
        response_body, status_code = profile_api.get_profile_followers(uuid, user_type)
        if status_code == 200:
            assert not response_body['profiles'], "API returned profiles for invalid user_type"
        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_validation_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    @pytest.mark.parametrize("limit, offset", [
        (10, -1),
        (-1, 10),
        (10, "ten"),
        ("ten", 10),
        (10, "^$#>/"),
        ("^$#>/", 10),
        (10, ""),
        ("", 10),
    ])
    def test_get_user_followers_invalid_limit_and_offset(self, authenticated_session,
                                                          uuid_retrieval, limit, offset):
        profile_api = Profile(authenticated_session)
        uuid = uuid_retrieval
        user_type = "all"
        response_body, status_code = profile_api.get_profile_followers(uuid, user_type, limit=limit, offset=offset)

        if status_code == 200:
            assert not response_body['profiles'], "API returned profiles for invalid limit/offset values"
        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_validation_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_user_followers_with_non_existing_user_profile_id(self, authenticated_session):
        profile_api = Profile(authenticated_session)
        uuid = "9fa85f64-5717-4562-b3fc-2c963f66afa6"
        response_body, status_code = profile_api.get_profile_followers(uuid, users_type="all")
        assert status_code == 404, f"Expected 404 for non existing user_profile_id, got {status_code} instead"

        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_not_found_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_user_followers_with_invalid_format_user_profile_id(self, authenticated_session, uuid_retrieval):
        profile_api = Profile(authenticated_session)
        uuid = "abc"
        response_body, status_code = profile_api.get_profile_followers(uuid, users_type="all")
        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"

        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_validation_error())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
