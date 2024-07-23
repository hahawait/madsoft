from fastapi import status

from apps.base.exceptions import AppException


class MemeNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Meme not found"
