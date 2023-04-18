from app.endpoints.auth import router as auth_router
from app.endpoints.user import router as user_router


routes = [auth_router, user_router]
