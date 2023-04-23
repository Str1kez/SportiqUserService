from datetime import datetime
from uuid import uuid4

# from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from .crypt import _decrypt_token, _encrypt_token
from app.config.jwt_settings import JWTSettings
from app.db.storage import Storage
from app.exceptions import InvalidToken, TokenIDUpcent, TokenInBlacklist, UserDeleted
from app.schema import CreatedTokens, Token
from app.tools import get_token_url


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


async def create_tokens(user_id: str) -> CreatedTokens:
    access_token = _create_token(user_id, "access")
    refresh_token = _create_token(user_id, "refresh")
    encrypted_access_token = await _encrypt_token(access_token)
    encrypted_refresh_token = await _encrypt_token(refresh_token)
    return CreatedTokens(access_token=encrypted_access_token, refresh_token=encrypted_refresh_token)


async def validate_token(token: str) -> Token:
    try:
        token_dto = await _decrypt_token(token)
    except JWTError as err:
        raise InvalidToken.factory(str(err))
    await _check_if_token_in_blacklist(token_dto)
    return token_dto


# async def get_validated_access_token(token_header: str = Depends(oauth2_scheme)) -> Token:
#     token_dto = await validate_token(token_header)
#     if token_dto.type_ != "access":
#         raise InvalidToken
#     return token_dto


async def _check_if_token_in_blacklist(decrypted_token: Token) -> None:
    if decrypted_token.jti == "":
        raise TokenIDUpcent
    kds_db = Storage().get_connection()
    entry = await kds_db.get("blacklist:key:" + decrypted_token.jti)
    if entry:
        raise TokenInBlacklist
    entry = await kds_db.get("blacklist:user:" + decrypted_token.user)
    if entry:
        raise UserDeleted


def _create_token(user_db_id: str, _type: str) -> Token:
    settings = JWTSettings()
    issued = datetime.utcnow()
    expire = issued + settings.access_expires
    jti = str(uuid4())
    token = Token(sub="auth", exp=expire, iat=issued, jti=jti, type=_type, user=user_db_id)
    return token
