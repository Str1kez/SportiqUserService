from pydantic import BaseModel, Field, SecretStr

from app.exceptions import InvalidPassword
from app.tools import verify_password


class Login(BaseModel):
    username: str = Field(..., min_length=6)
    password: SecretStr = Field(..., min_length=8)

    def to_orm(self) -> dict:
        user = self.dict()
        user["password"] = user["password"].get_secret_value()
        return user

    def validate_password(self, hashed_password: str) -> None:
        if not verify_password(self.password.get_secret_value(), hashed_password):
            raise InvalidPassword(detail="You entered invalid password")
