from typing import Any, Self

from fastapi import HTTPException, status


class InvalidToken(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = [{"msg": "Неверный токен", "type": "unknown"}],
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)

    @classmethod
    def factory(cls, message: str) -> Self:
        match message:
            case "Signature has expired.":
                return InvalidToken(detail=[{"msg": message, "type": "expired"}])
            case "Signature verification failed.":
                return InvalidToken(detail=[{"msg": message, "type": "unverified"}])
        return InvalidToken()


class TokenInBlacklist(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = [{"msg": "Токен утилизирован", "type": "blacklist"}],
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)


class TokenIDUpcent(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = [{"msg": "JTI отсутствует", "type": "jti_upcent"}],
        headers: dict[str, Any] | None = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)
