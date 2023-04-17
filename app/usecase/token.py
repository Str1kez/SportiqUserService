from fastapi_jwt_auth import AuthJWT

from app.db.storage import Storage
from app.exceptions.auth import SecretKeyNotFound
from app.schema import CreatedTokens, UserDTO


async def get_secret_key():
    kds_db = Storage().get_connection()
    secret_key = await kds_db.get("secret_key")
    if secret_key is None:
        raise SecretKeyNotFound
    return secret_key


def create_tokens(user: UserDTO, auth: AuthJWT, secret_key: str) -> CreatedTokens:
    auth._secret_key = secret_key
    access_token = auth.create_access_token(subject=user.username)
    refresh_token = auth.create_refresh_token(subject=user.username)
    return CreatedTokens(access_token=access_token, refresh_token=refresh_token)


async def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token.get("jti")
    if jti is None:
        print("jti is upcent")
    kds_db = Storage().get_connection()
    entry = await kds_db.get(jti)
    return entry and entry == "true"


# TODO: Создать класс для работы с JWT
