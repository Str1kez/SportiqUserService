from fastapi import APIRouter, Cookie, Header, Response, status
from fastapi.security import OAuth2PasswordBearer

from app.exceptions import InvalidToken
from app.schema import CreatedTokens
from app.tools import get_token_url, move_to_blacklist
from app.usecase.token import create_token, validate_token


router = APIRouter(tags=["Auth", "Token"], prefix="/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.post(
    "/refresh", response_model=CreatedTokens, status_code=status.HTTP_201_CREATED, description="Token refreshing"
)
async def refresh(response: Response, refresh_token: str = Cookie(..., alias="refreshToken")) -> CreatedTokens:
    token_dto = await validate_token(refresh_token)
    if token_dto.type_ != "refresh":
        raise InvalidToken
    await move_to_blacklist(token_dto.jti, "key")
    access_token = CreatedTokens(access_token=await create_token(token_dto.user, "access"))
    refresh_token = await create_token(token_dto.user, "refresh")
    response.set_cookie("refreshToken", refresh_token, httponly=True, domain="api.sportiq.org")
    return access_token


@router.post(
    "/access-revoke",
    response_class=Response,
    status_code=status.HTTP_200_OK,
    description="Revoking access token, **need to be authenticated by API Gateway**",
)
async def access_revoke(token_jti: str = Header(..., alias="Token")) -> None:
    await move_to_blacklist(token_jti, "key")


@router.post(
    "/refresh-revoke", response_class=Response, status_code=status.HTTP_200_OK, description="Revoking refresh token"
)
async def refresh_revoke(refresh_token: str = Cookie(..., alias="refreshToken")) -> None:
    token_dto = await validate_token(refresh_token)
    if token_dto.type_ != "refresh":
        raise InvalidToken
    await move_to_blacklist(token_dto.jti, "key")
