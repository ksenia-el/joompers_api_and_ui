import pytest
from api.api_library.user_account import UserAccount
from api.conftest import user_not_logged_in_session_fixture
from api.support.temporary_email_generator import EmailAndPasswordGenerator


class TestDeleteUser:

    def test_delete_user_positive(self, user_not_logged_in_session_fixture):
        # ----- precondition: create a user account first
        email_and_password_generator = EmailAndPasswordGenerator()
        username, email, password = email_and_password_generator.generate_username_and_email_and_password()

        session = user_not_logged_in_session_fixture
        api = UserAccount(session)
        request_user_registration = api.user_registration(username, email, password)

        response_body = request_user_registration[0]

        status = request_user_registration[1]
        assert status == 201

        confirmation_token_from_email = email_and_password_generator.get_token_from_confirmation_link_for_registration()
        assert confirmation_token_from_email is not None
        request_confirm_user_registration = api.confirm_email(confirmation_token_from_email)
        status = request_confirm_user_registration[1]
        assert status == 200

        # now to have a session of user being authorized
        request_log_in_with_email = api.log_in_with_email(email, password)
        response, status = request_log_in_with_email
        assert status == 200
        access_token = response.get("access_token")
        session.headers.update(
            {"Authorization": f"Bearer {access_token}"})  # by that we update session, so now the user is logged in

        # and also having a process of deleting user being started
        api = UserAccount(session)
        response, status = api.request_delete_user()
        assert status == 200
        code_from_email_to_confirm = email_and_password_generator.get_confirmation_code_for_delete_user()
        assert code_from_email_to_confirm is not None

        # --- now the test itself
        request_confirm_delete_user = api.delete_user(code_from_email_to_confirm)
        response, status = request_confirm_delete_user
        expected_response_body = {'message': 'Successfully deleted'}
        assert status == 200
        assert response == expected_response_body

        # additional check that after being deleted user can't log in as usual
        session.headers.pop("Authorization", None)  # by that we update session object, so now user is not authorized
        api = UserAccount(session)
        request_log_in_with_email = api.log_in_with_email(email, password)
        response, status = request_log_in_with_email
        expected_response_body = {'code': 'not_found_error', 'message': 'User has been banned or deleted'}
        assert status == 404
        assert response == expected_response_body

        # ----- now we just delete email address created in the test before - tear-down
        email_and_password_generator.delete_email_generated()


    # try to delete user with a valid confirmation code while being not authenticated
    def test_delete_user_not_authenticated_negative(self, user_not_logged_in_session_fixture):
        # ----- precondition: create a user account first
        email_and_password_generator = EmailAndPasswordGenerator()
        username, email, password = email_and_password_generator.generate_username_and_email_and_password()

        session = user_not_logged_in_session_fixture
        api = UserAccount(session)
        request_user_registration = api.user_registration(username, email, password)
        status = request_user_registration[1]
        assert status == 201

        confirmation_token_from_email_for_registration = email_and_password_generator.get_token_from_confirmation_link_for_registration()
        assert confirmation_token_from_email_for_registration is not None
        request_confirm_user_registration = api.confirm_email(confirmation_token_from_email_for_registration)
        status = request_confirm_user_registration[1]
        assert status == 200

        # now to have a session of user being authorized
        request_log_in_with_email = api.log_in_with_email(email, password)
        response, status = request_log_in_with_email
        assert status == 200
        access_token = response.get("access_token")
        session.headers.update(
            {"Authorization": f"Bearer {access_token}"})  # by that we update session, so now the user is logged in

        # and also having a process of deleting user being started
        api = UserAccount(session)
        response, status = api.request_delete_user()
        assert status == 200
        code_from_email_to_confirm_delete = email_and_password_generator.get_confirmation_code_for_delete_user()
        assert code_from_email_to_confirm_delete is not None

        # --- now the test itself
        session.headers.pop("Authorization", None)  #  so the session is not authorized now
        # api = UserAccount(session)
        request_confirm_delete_user = api.delete_user(code_from_email_to_confirm_delete)
        response, status = request_confirm_delete_user

        expected_response_body = {'detail': 'Not authenticated'}
        assert status == 401
        assert response == expected_response_body

        # also check that the user account was not deleted
        request_user_log_in = api.log_in_with_email(email, password)
        status = request_user_log_in[1]
        assert status == 200

        # ----- now we just delete user account and email address created in the test before - tear-down
        session.headers.update(
            {"Authorization": f"Bearer {access_token}"})  # by that we update session, so now the user is logged in
        request_confirm_delete_user = api.delete_user(code_from_email_to_confirm_delete)
        status = request_confirm_delete_user[1]
        assert status == 200

        email_and_password_generator.delete_email_generated()

