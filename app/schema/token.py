from pydantic import BaseModel, Field


class CreatedTokens(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")

    class Config:
        allow_population_by_field_name = True
