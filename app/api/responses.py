"""Общие ответы для документации API."""

UNAUTHORIZED_RESPONSE = {
    401: {
        "description": "Неверный API ключ",
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated"}
            }
        },
    },
}
