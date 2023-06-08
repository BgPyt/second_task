import uuid
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users import FastAPIUsers
from fastapi_users.authentication.transport.bearer import BearerResponse
from fastapi_users.openapi import OpenAPIResponseType
from starlette.responses import Response, JSONResponse
from config import REDIS_HOST, REDIS_PORT
from src.auth.manage import get_user_manager
from src.auth.models import User
from fastapi_users.authentication import BearerTransport
import redis.asyncio
from fastapi_users.authentication import RedisStrategy
from fastapi import status


redis = redis.asyncio.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

class SchemeBearer(BearerResponse):
    access_token: str
    token_type: str
    UUID: str


class BearerAnswer(BearerTransport):

    async def get_login_response(self, token: str) -> Response:
        UUID = await redis.get(f"fastapi_users_token:{token}")
        bearer_response = SchemeBearer(access_token=token, token_type="bearer", UUID=str(UUID))
        return JSONResponse(bearer_response.dict())

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "token_type": "bearer",
                            "UUID": "eb3c5ce4-b08f-4341-bba1-42241b606ab5"
                        }
                    }
                },
            },
        }


bearer_transport = BearerAnswer(tokenUrl="auth/jwt/login")

SECRET = "SECRET"


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

