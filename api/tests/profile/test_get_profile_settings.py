import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema

class TestGetProfileSettings:
    @allure.feature("Get user settings")
    @allure.severity('Major')
    def test_get_profile_settings_success(self, authenticated_session):
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_settings()
        assert status_code == 200, "Failed to get user settings"
        try:
            validate(instance=response_body, schema=schema.get_settings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"