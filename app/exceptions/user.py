from typing import Any, Self

from fastapi import HTTPException, status


class UserExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = [{"msg": "Пользователь с такими данными уже есть", "type": "user"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)

    @classmethod
    def factory(cls, message: str) -> Self:
        if "ix__user__username" in message:
            return UserExists(detail=[{"msg": "Пользователь с таким ником уже существует", "type": "user.username"}])
        if "ix__user__phone_number" in message:
            return UserExists(
                detail=[{"msg": "Пользователь с таким телефоном уже существует", "type": "user.phone_number"}]
            )
        return UserExists()


class UserNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = [{"msg": "Пользователь не найден", "type": "user"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class UserDeleted(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_410_GONE,
        detail: Any = [{"msg": "Пользователь удален", "type": "user"}],
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
