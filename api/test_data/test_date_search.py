import jsonschema
import json

def validate_search_response(data):
    # JSON-схема для SearchResponse
    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "searchProfile": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "const": "Searchprofile"},
                        "UserProfile": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"},
                                "id": {"type": "string", "format": "uuid"},
                                "userId": {"type": "string", "format": "uuid"},
                                "name": {"type": "string"},
                                "username": {"type": "string"},
                                "photoUrl": {"type": "string"},
                            },
                            "required": ["id", "userId", "name", "username"],
                        },
                    },
                    "required": ["title", "UserProfile"],
                },
            },
            "searchHashtags": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["searchProfile", "searchHashtags"],
    }

    # Валидация данных по схеме
    jsonschema.validate(data, schema)
