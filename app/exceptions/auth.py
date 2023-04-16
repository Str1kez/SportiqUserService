from typing import Any

from fastapi import HTTPException, status


class InvalidPassword(HTTPException):
    def __init__(
        self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: Any = None, headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__(status_code, detail, headers)
