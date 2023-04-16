from pydantic import Field

from app.schema.login import Login
from app.tools import get_password_hash


class UserDTO(Login):
    first_name: str = Field(..., min_length=2, alias="firstName")
    last_name: str = Field(..., min_length=2, alias="lastName")

    def to_dict_with_hashed_password(self) -> dict:
        user = self.to_orm()
        user["password"] = get_password_hash(user["password"])
        return user

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
