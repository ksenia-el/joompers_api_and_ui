from api.api_library.user_account import UserAccount
from api.conftest import new_user_logged_in_session_and_data_fixture
import allure


class TestUserLogOut:

    @allure.feature('User log out')
    @allure.description('User authenticated logs out')
    @allure.severity('Critical')
    def test_user_log_out_positive(self, new_user_logged_in_session_and_data_fixture):
        session, email, password, user_profile_id, user_role, user_status = new_user_logged_in_session_and_data_fixture
        api = UserAccount(session)  # create an Endpoints instance using a session of authorized user
        response_body, status = api.user_logout()
        message = response_body.get("message")
        assert status == 200
        assert message == "You have been logout"

