from jose import jwt

from app.config.jwt_settings import JWTSettings
from app.schema import Token


async def _encrypt_token(token: Token) -> str:
    settings = JWTSettings()
    secret_key = await settings.get_secret_key()
    encoded_jwt = jwt.encode(token.dict(), secret_key, settings.algorithm)
    return encoded_jwt


async def _decrypt_token(token: str) -> Token:
    settings = JWTSettings()
    secret_key = await settings.get_secret_key()
    encoded_jwt = jwt.decode(token, secret_key, settings.algorithm)
    return Token(**encoded_jwt)
