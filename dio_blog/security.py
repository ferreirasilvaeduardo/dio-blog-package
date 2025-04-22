import time
from typing import Annotated, Any, Optional  # , Any, Coroutine
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from dio_blog.config import settings  # noqa


class AccessToken(BaseModel):
    iss: str
    sub: int | str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: AccessToken


def sign_jwt(user_id: int | str) -> JWTToken | dict[str, str]:
    now = time.time()
    payload = {
        "iss": settings.ISS,
        "sub": str(user_id),
        "aud": str(settings.AUD).strip(),
        "exp": now + (60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token}


async def decode_jwt(token: str) -> Optional[JWTToken]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            audience=str(settings.AUD).strip(),
            algorithms=[settings.ALGORITHM],
        )
        _token = JWTToken.model_validate({"access_token": decoded_token})
        return _token if _token.access_token.exp >= time.time() else None
    except Exception:  # as erro:
        # import traceback
        # print(
        #     f"ERRO \n------------------------------"
        #     f"\nFalha no Processo {erro} "
        #     f"\n----------------  FALHA  ------------"
        #     f"\n\n traceback:\n{traceback.format_exc()}"
        # )
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials | None | Any]:  # JWTToken:  # | None | Optional[HTTPAuthorizationCredentials] | Any:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not str(scheme).strip().upper() == str(settings.SCHEME).strip().upper():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token.",
                )
            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )


async def get_current_user(
    token: Annotated[JWTToken, Depends(JWTBearer())],
) -> dict[str, int] | Any:
    return {"user_id": token.access_token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user
