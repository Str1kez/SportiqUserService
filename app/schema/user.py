from pydantic import BaseModel, Field, SecretStr, constr

from app.tools.password_hash import get_password_hash


class User(BaseModel):
    username: str
    phone_number: str = Field(..., alias="phoneNumber")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserUpdate(BaseModel):
    username: str | None = Field(min_length=6)
    phone_number: constr(strip_whitespace=True, regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$") | None = Field(
        alias="phoneNumber"
    )
    password: SecretStr | None = Field(min_length=8)
    first_name: str | None = Field(alias="firstName")
    last_name: str | None = Field(alias="lastName")

    def prepared_dict(self):
        data = self.dict(exclude_none=True)
        if "password" in data:
            data["password"] = get_password_hash(data["password"].get_secret_value())
        return data
