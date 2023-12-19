import allure
import pytest

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data
"""
Bug Report: BJT-154, 156, 157

Note: 
- There are many bugs and ambiguities here, so the tests will be revised later.
- "Username must contain from 3 to 32 symbols (numbers, letters or '.' are allowed)",
- Sex Must be Male, Female or Other'
"""
@allure.feature("Get update profile")
@allure.severity("Normal")
class TestUpdateProfile:

    def test_update_profile_country_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"country": "France"}
        response_body, status_code = profile_api.update_profile(data=update_data)
        print(response_body)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("country") == update_data["country"], "Country did not update correctly"

    def test_update_profile_name_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"name": "New Name"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("name") == update_data["name"], "Name did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_username_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"username": "newUserName12"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update username, got {status_code} code"
        assert response_body.get("username") == update_data["username"], "Username did not update correctly"

    def test_update_profile_sex_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"sex": "Female"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update sex, got {status_code} code"
        assert response_body.get("sex") == update_data["sex"], "Sex did not update correctly"

    def test_update_profile_bio_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"bio": "new bio"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update bio, got {status_code} code"
        assert response_body.get("bio") == update_data["bio"], "Bio did not update correctly"

    def test_update_profile_profession_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"professionId": data.profession_id_music}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update professionId, got {status_code} code"
        assert response_body.get("professionId") == update_data["professionId"], "ProfessionId did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_photo_url_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"photoUrl": "https://poroda-mops.ru/wp-content/uploads/2017/06/kak-pravilno-vybrat-shhenka-mopsa.jpg"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update photoUrl, got {status_code} code"
        assert response_body.get("photoUrl") == update_data["photoUrl"], "photoUrl did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_background_picture_url_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"backgroundPictureUrl": "https://vashkinolog.com/wp-content/uploads/2017/10/mopsiki_foto_shenki_1-360x270.jpg"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("backgroundPictureUrl") == update_data["backgroundPictureUrl"], "backgroundPictureUrl did not update correctly"
    def test_update_profile_chat_message_notify_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"chatMessageNotify": False}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("chatMessageNotify") == update_data["chatMessageNotify"], "chatMessageNotify did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_with_empty_values_successful(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        empty_values = data.update_profile_empty_values
        response_body, status_code = profile_api.update_profile(data=empty_values)
        success_message = response_body.get("message")
        print(response_body)

        assert status_code == 200, f"Failed to update profile, got {status_code} code"


    def test_update_profile_unauthorized(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        update_data = {"country": "France"}
        response_body, status_code = profile_api.update_profile(data=update_data)
        error_message = response_body["detail"]

        assert status_code == 401, f"Expected 401 for unauthorized user, got {status_code} instead"
        assert error_message == "Not authenticated"

