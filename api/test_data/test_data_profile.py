class ProfileJsonSchemas:
    @staticmethod
    def get_followers_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "userId": {"type": "string"},
                            "name": {"type": "string"},
                            "username": {"type": "string"},
                            "photoUrl": {"type": ["string", "null"]},
                            "bio": {"type": ["string", "null"]},
                            "role": {"type": "string"}
                        },
                        "required": ["id", "userId", "name", "username", "role"]
                    }
                },
                "count": {"type": "integer"}
            },
            "required": ["profiles", "count"]
        }
    @staticmethod
    def get_followers_response_schema_validation_error():
        return {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "msg": {
                                    "type": "string"
                                },
                                "type": {
                                    "type": "string"
                                }
                            },
                            "required": ["loc", "msg", "type"]
                        }
                    }
                },
                "required": ["detail"]
            }

    @staticmethod
    def get_followers_response_schema_not_found_error():
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                }
            },
            "required": ["code", "message"]
        }


    @staticmethod
    def get_followings_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "userId": {"type": "string"},
                            "name": {"type": "string"},
                            "username": {"type": "string"},
                            "photoUrl": {"type": "string"},
                            "bio": {"type": "string"}
                        },
                        "required": ["id", "userId", "name", "username", "photoUrl", "bio"]
                    }
                },
                "count": {"type": "integer"}
            },
            "required": ["profiles", "count"]
        }
    @staticmethod
    def get_settings_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "country": {
                    "type": ["string", "null"]
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "sex": {
                    "type": ["string", "null"]
                },
                "profession": {
                    "type": ["string", "null"]
                },
                "chatMessageNotify": {
                    "type": "boolean"
                },
                "allCountries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "string"
                            },
                            "label": {
                                "type": "string"
                            }
                        },
                        "required": ["value", "label"]
                    }
                }
            },
            "required": ["email", "chatMessageNotify"]
        }

    @staticmethod
    def get_profile_creator_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid"
                },
                "userId": {
                    "type": "string",
                    "format": "uuid"
                },
                "name": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "photoUrl": {
                    "type": ["string", "null"]
                },
                "bio": {
                    "type": ["string", "null"]
                },
                "backgroundPictureUrl": {
                    "type": ["string", "null"]
                },
                "socialDataBlock": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "socialNetworkId": {
                                "type": "string",
                                "format": "uuid"
                            },
                            "socialNetworkIconUrl": {
                                "type": "string"
                            },
                            "socialNetworkTitle": {
                                "type": "string"
                            },
                            "socialNetworkUserValue": {
                                "type": ["string", "null"]
                            }
                        },
                        "required": ["socialNetworkId", "socialNetworkIconUrl", "socialNetworkTitle"]
                    }
                },
                "profession": {
                    "type": ["string", "null"]
                },
                "followers": {
                    "type": "integer"
                },
                "followings": {
                    "type": "integer"
                },
                "isFollowedByCurrentUser": {
                    "type": "boolean",
                },
                "isBlockedByCurrentUser": {
                    "type": "boolean"
                },
                "isBlockedByUser": {
                    "type": "boolean"
                }
            },
            "required": [
                "id",
                "userId",
                "name",
                "username",
                "socialDataBlock",
                "isBlockedByCurrentUser",
                "isBlockedByUser"
            ]
        }
    @staticmethod
    def get_profile_user_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The unique identifier for the user profile."
                },
                "userId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The unique identifier for the user."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the user."
                },
                "username": {
                    "type": "string",
                    "description": "The username for the user profile."
                },
                "photoUrl": {
                    "type": ["string", "null"],
                    "description": "The URL to the user's photo."
                },
                "isBlockedByCurrentUser": {
                    "type": "boolean",
                    "description": "Indicates if the user is blocked by the current user."
                },
                "isBlockedByUser": {
                    "type": "boolean",
                    "description": "Indicates if the user has been blocked by another user."
                }
            },
            "required": ["id", "userId", "name", "username"]
        }
