from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.recipes import router as recipes_router
from routers.comments import router as comments_router

routers = [auth_router, users_router, recipes_router, comments_router]
