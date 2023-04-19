from pydantic import Field, constr

from app.schema.login import Login
from app.tools import get_password_hash


class SignUp(Login):
    phone_number: constr(strip_whitespace=True, regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$") = Field(
        ..., alias="phoneNumber"
    )
    first_name: str = Field(..., min_length=2, alias="firstName")
    last_name: str = Field(..., min_length=2, alias="lastName")

    def to_dict_with_hashed_password(self) -> dict:
        user = self.to_orm()
        user["password"] = get_password_hash(user["password"])
        return user

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
