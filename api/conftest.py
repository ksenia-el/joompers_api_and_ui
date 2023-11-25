import pytest
from api.api_library.user_account import UserAccount
import requests
from api.test_data.test_data_user_account import TestData


# fixture to create a session with user being authenticated
#  used when an instance of Endpoints-class is created (to run API-calls that need authorization)
@pytest.fixture()
def user_logged_in_session_fixture():
    session = requests.Session()
    api = UserAccount(session)
    response_body, status = api.log_in_with_email(TestData.valid_user_credentials[0]["email"], TestData.valid_user_credentials[0]["password"])
    access_token = response_body.get("access_token")
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


