from fastapi import FastAPI
from app.core.db import Base, engine
from app.core.seed import seed_superadmin

# import routers
from .register_routes import register_all_routes

# create fastapi app
app = FastAPI()

# connect db & tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    seed_superadmin()

# connect all routes here
app.include_router(register_all_routes)