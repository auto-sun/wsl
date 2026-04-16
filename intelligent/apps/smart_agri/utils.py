from rest_framework import status
from rest_framework.response import Response


def api_success(data=None, message="ok", status_code=status.HTTP_200_OK):
    return Response(
        {
            "code": 0,
            "message": message,
            "data": data if data is not None else {},
        },
        status=status_code,
    )


def api_error(message, code=1, status_code=status.HTTP_400_BAD_REQUEST, extra=None):
    payload = {
        "code": code,
        "message": message,
        "data": extra or {},
    }
    return Response(payload, status=status_code)
