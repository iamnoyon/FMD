from fastapi import APIRouter

# import all routers
from app.modules.auth.router import router as auth_router
from app.modules.categories.route import router as categories_router
from app.modules.upload.route import router as upload_router
from app.modules.product.route import router as product_router

# create main route
register_all_routes = APIRouter()

# register all routes
register_all_routes.include_router(auth_router)
register_all_routes.include_router(categories_router)
register_all_routes.include_router(product_router)
register_all_routes.include_router(upload_router)

