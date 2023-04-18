from datetime import timedelta

from pydantic import BaseModel

from app.db.storage import Storage
from app.exceptions import SecretKeyNotFound


class JWTSettings(BaseModel):
    # TODO: Добавить еще параметров
    access_expires: timedelta = timedelta(minutes=15)
    refresh_expires: timedelta = timedelta(days=30)
    algorithm = "HS256"

    async def get_secret_key(self):
        kds_db = Storage().get_connection()
        secret_key = await kds_db.get("secret_key")
        if secret_key is None:
            raise SecretKeyNotFound
        return secret_key
