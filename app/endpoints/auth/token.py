from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer

from app.exceptions import InvalidToken
from app.schema import CreatedTokens, RefreshRequest
from app.tools import get_token_url
from app.usecase.token import create_tokens, move_to_blacklist, validate_token


router = APIRouter(tags=["Auth", "Token"], prefix="/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.post("/refresh", response_model=CreatedTokens, status_code=status.HTTP_201_CREATED)
async def refresh(token_request: RefreshRequest) -> CreatedTokens:
    token_dto = await validate_token(token_request.refresh_token)
    if token_dto.type_ != "refresh":
        raise InvalidToken
    await move_to_blacklist(token_dto.jti)
    new_tokens = await create_tokens(token_dto.user)
    return new_tokens


@router.post("/access-revoke", response_class=Response, status_code=status.HTTP_200_OK)
async def access_revoke(token_header: str = Depends(oauth2_scheme)) -> None:
    print(token_header)
    token_dto = await validate_token(token_header)
    if token_dto.type_ != "access":
        raise InvalidToken
    await move_to_blacklist(token_dto.jti)


@router.post("/refresh-revoke", response_class=Response, status_code=status.HTTP_200_OK)
async def refresh_revoke(token_request: RefreshRequest) -> None:
    token_dto = await validate_token(token_request.refresh_token)
    if token_dto.type_ != "refresh":
        raise InvalidToken
    await move_to_blacklist(token_dto.jti)
