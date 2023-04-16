from typing import Any

from fastapi import HTTPException, status


class DBError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class UserNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = "User with this username not found",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
