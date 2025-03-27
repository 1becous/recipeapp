from .auth import router as auth_router
from .users import router as users_router
from .recipes import router as recipes_router
from .comments import router as comments_router

routers = [auth_router, users_router, recipes_router, comments_router]
