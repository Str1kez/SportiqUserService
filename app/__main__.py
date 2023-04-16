from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.config import DefaultSettings
from app.db.cache import Cache
from app.endpoints import routes


def bind_routes(app: FastAPI):
    path_prefix = DefaultSettings().PATH_PREFIX
    for router in routes:
        app.include_router(router, prefix=path_prefix)


def add_cors(app: FastAPI):
    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def check_db_connection(_: FastAPI):
    # TODO: ping redis
    settings = DefaultSettings()
    yield


app = FastAPI(lifespan=check_db_connection)
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    settings = DefaultSettings()
    run("app.__main__:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, reload_dirs=["app"])
