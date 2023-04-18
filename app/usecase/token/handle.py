from datetime import datetime
from uuid import uuid4

from .crypt import _encrypt_token
from app.config.jwt_settings import JWTSettings
from app.db.storage import Storage
from app.schema import CreatedTokens, Token


async def create_tokens(user_id: str) -> CreatedTokens:
    access_token = _create_token(user_id, "access")
    refresh_token = _create_token(user_id, "refresh")
    encrypted_access_token = await _encrypt_token(access_token)
    encrypted_refresh_token = await _encrypt_token(refresh_token)
    return CreatedTokens(access_token=encrypted_access_token, refresh_token=encrypted_refresh_token)


async def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token.get("jti")
    if jti is None:
        print("jti is upcent")
    kds_db = Storage().get_connection()
    entry = await kds_db.get(jti)
    return entry and entry == "true"


def _create_token(user_db_id: str, _type: str) -> Token:
    settings = JWTSettings()
    issued = datetime.utcnow()
    expire = issued + settings.access_expires
    jti = str(uuid4())
    token = Token(sub="auth", exp=expire, iat=issued, jti=jti, type=_type, user=user_db_id)
    return token
