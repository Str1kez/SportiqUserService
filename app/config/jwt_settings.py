from datetime import timedelta

from pydantic import BaseModel


class JWTSettings(BaseModel):
    # TODO: Добавить еще параметров
    access_expires: timedelta = timedelta(minutes=15)
    refresh_expires: timedelta = timedelta(days=30)
