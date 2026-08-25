from fastapi import APIRouter

# import all routers
from app.modules.auth.router import router as auth_router

# create main route
register_all_routes = APIRouter()

# register all routes
register_all_routes.include_router(auth_router)

