import pytest
from api.api_library.user_account import UserAccount
import requests
from api.api_library.conversation import Conversation
from api.test_data.test_data_user_account import TestData
import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Loading required variables from the .env file
VALID_EMAIL = os.environ["VALID_EMAIL"]
VALID_PASSWORD = os.environ["VALID_PASSWORD"]
# CLIENT_ID = os.environ["CLIENT_ID"]
# CLIENT_SECRET = os.environ["CLIENT_SECRET"]
# SCOPE = os.environ.get("SCOPE", "") 

@pytest.fixture(scope="session")
def authenticated_session():
    session = requests.Session()
    # Data preparation for the query
    login_data = {
        "grant_type": "password",
        "username": VALID_EMAIL,
        "password": VALID_PASSWORD,
        # "scope": SCOPE,
        # "client_id": CLIENT_ID,
        # "client_secret": CLIENT_SECRET
    }

    # Executing the login request
    response = session.post(
        "https://api.dev.joompers.com/api/login/oauth",
        data=login_data
    )

    # Checking for a successful response status
    assert response.status_code == 200, f"Failed to log in: {response.text}"

    # Retrieving the access token and adding it to the session headers.
    access_token = response.json().get("access_token")
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    return session

#fixture to get chat_id
@pytest.fixture(scope="session")
def chat_id_session():
    session = requests.Session()
    login_data = {
        "grant_type": "password",
        "username": VALID_EMAIL,
        "password": VALID_PASSWORD,
    }

    response = session.post(
        "https://api.dev.joompers.com/api/login/oauth",
        data=login_data
    )

    assert response.status_code == 200, f"Failed to log in: {response.text}"
    access_token = response.json().get("access_token")
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    return session

@pytest.fixture(scope="session")
def chat_id(chat_id_session):
    conversation_api = Conversation(chat_id_session)
    response_json, status_code = conversation_api.chat_list({"limit": 100, "offset": 0})
    assert status_code == 200, "Failed to retrieve chat list"
    return response_json[0]['chatInfo']['id']

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
