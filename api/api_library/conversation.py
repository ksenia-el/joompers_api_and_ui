import requests
import allure
from json.decoder import JSONDecodeError


class Conversation:
    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session

    @allure.step('Get chat list')
    def chat_list(self, params):
        limit = params.get("limit")
        offset = params.get("offset")
        url = f"{self.base_url}/api/conversation/chats?limit={limit}&offset={offset}"
        response = self.session.get(url)
        status = response.status_code

        if status == 200:
            try:
                response_data = response.json()
            except JSONDecodeError:
                response_data = {"error": "Invalid JSON response"} 
        else:
            response_data = {
                "error": response.text,
                "status_code": status
            }

        return response_data, status

    @allure.step('Get chat list with chat ID')
    def chat_list_with_chatId(self, chat_id, limit, offset):
        url = f"{self.base_url}/api/conversation/chat/{chat_id}?limit={limit}&offset={offset}"
        response = self.session.get(url)
        status = response.status_code

        if status == 200:
            try:
                response_data = response.json()
            except JSONDecodeError:
                response_data = {"error": "Invalid JSON response"} 
        else:
            response_data = {
                "error": response.text,
                "status_code": status
            }

        return response_data, status

    @allure.step('Send message with chatId')
    def chat_with_chatId_post_message(self, chat_id, message):
        url = f"{self.base_url}/api/conversation/chat/{chat_id}/send_message"

        data = {
            "message": message
        }
   
        response = self.session.post(url, json=data)
        status = response.status_code

        if status == 201:
            try:
                response_data = response.json()
            except JSONDecodeError:
                response_data = {"error": "Invalid JSON response"} 
        else:
            response_data = {
                "error": response.text,
                "status_code": status
            }

        return response_data, status
