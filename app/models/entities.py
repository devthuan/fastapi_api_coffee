

from enum import Enum


def generate_response(status: str, code: int, message: str, data: dict = None):
    response = {"status": status, "code": code, "message": message}
    if data is not None:
        response["data"] = data
    return response

class ResponseStatus(str, Enum):
    VALIDATION_ERROR = "Validation Error"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    NOT_FOUND = "Not Found"
    UNAUTHORIZED = "Unauthorized"