from fastapi import HTTPException, status


class AppException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Common app exception"
    headers = None

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers
        )
