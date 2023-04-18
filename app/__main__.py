from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.config import DefaultSettings
from app.db.storage import Storage
from app.endpoints import routes
from app.tools import generate_secret_key


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
async def init_secret_key(_: FastAPI):
    kds_db = Storage().get_connection()
    secret_key = generate_secret_key()
    await kds_db.setnx("secret_key", secret_key)
    yield


app = FastAPI(lifespan=init_secret_key, root_path=f"http://{DefaultSettings().APP_HOST}:{DefaultSettings().APP_PORT}")
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    settings = DefaultSettings()
    run("app.__main__:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, reload_dirs=["app"])
