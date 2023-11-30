class TestData:
    @classmethod
    def get_expected_response(cls):
        return [
            {
                "chatInfo": {
                    "id": str,
                    "type": str,
                    "isBlocked": bool,
                    "companion": {
                        "profile": {
                            "id": str,
                            "userId": str,
                            "name": str,
                            "username": str,
                            "photoUrl": (str, type(None)),  # Может быть строкой или None
                            "isBlockedByCurrentUser": bool,
                            "isBlockedByUser": bool
                        }
                    }
                },
                "lastMessage": {
                    "id": str,
                    "message": str,
                    "profile": {
                        "id": str,
                        "userId": str,
                        "name": str,
                        "username": str,
                        "photoUrl": (str, type(None))  # Может быть строкой или None
                    },
                    "createdAt": str
                },
                "countMessages": int,
                "unreadCount": (int, type(None))  # Может быть целым числом или None
            },
            {
                "chatInfo": {
                    "id": str,
                    "type": str,
                    "isBlocked": bool,
                    "companion": {
                        "profile": {
                            "id": str,
                            "userId": str,
                            "name": str,
                            "username": str,
                            "photoUrl": (str, type(None)),  # Может быть строкой или None
                            "isBlockedByCurrentUser": bool,
                            "isBlockedByUser": bool
                        }
                    }
                },
                "messages": [
                    {
                        "id": str,
                        "message": str,
                        "profile": {
                            "id": str,
                            "userId": str,
                            "name": str,
                            "username": str,
                            "photoUrl": (str, type(None)),  # Может быть строкой или None
                        },
                        "createdAt": str,
                        "currentUserView": bool,
                        "companionView": bool,
                        "incoming": bool
                    }
                ]
            },
            {
                "message": "Successfully sent message"
            },
            {
                "detail": "Chat with this id does not exist in your chats"
            }
        ]
