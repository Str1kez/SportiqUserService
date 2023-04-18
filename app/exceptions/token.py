from typing import Any

from fastapi import HTTPException, status


class InvalidToken(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Неверный токен",
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class TokenInBlacklist(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Токен уже утилизирован",
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class TokenIDUpcent(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Токен без id",
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)
