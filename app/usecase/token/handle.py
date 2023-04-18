from datetime import datetime
from uuid import uuid4

from jose import JWTError

from .crypt import _decrypt_token, _encrypt_token
from app.config.jwt_settings import JWTSettings
from app.db.storage import Storage
from app.exceptions import InvalidToken
from app.exceptions.token import TokenIDUpcent, TokenInBlacklist
from app.schema import CreatedTokens, Token


async def create_tokens(user_id: str) -> CreatedTokens:
    access_token = _create_token(user_id, "access")
    refresh_token = _create_token(user_id, "refresh")
    encrypted_access_token = await _encrypt_token(access_token)
    encrypted_refresh_token = await _encrypt_token(refresh_token)
    return CreatedTokens(access_token=encrypted_access_token, refresh_token=encrypted_refresh_token)


async def validate_token(token: str) -> Token:
    try:
        token_dto = await _decrypt_token(token)
    except JWTError:
        raise InvalidToken
    await check_if_token_in_blacklist(token_dto)
    return token_dto


async def check_if_token_in_blacklist(decrypted_token: Token) -> None:
    if decrypted_token.jti == "":
        raise TokenIDUpcent
    kds_db = Storage().get_connection()
    entry = await kds_db.get("blacklist:" + decrypted_token.jti)
    if entry:
        raise TokenInBlacklist


async def move_to_blacklist(jti: str) -> None:
    kds_db = Storage().get_connection()
    await kds_db.set("blacklist:" + jti, 1)


def _create_token(user_db_id: str, _type: str) -> Token:
    settings = JWTSettings()
    issued = datetime.utcnow()
    expire = issued + settings.access_expires
    jti = str(uuid4())
    token = Token(sub="auth", exp=expire, iat=issued, jti=jti, type=_type, user=user_db_id)
    return token
