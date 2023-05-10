from datetime import datetime

from pydantic import BaseModel, Field


class CreatedTokens(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    # refresh_token: str = Field(..., alias="refreshToken")

    class Config:
        allow_population_by_field_name = True


class Token(BaseModel):
    sub: str
    exp: datetime
    iat: datetime
    jti: str
    type_: str = Field(..., alias="type")
    user: str
