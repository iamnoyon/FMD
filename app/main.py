from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import Base, engine, auto_sync_schema
from app.core.seed import seed_superadmin

# import routers
from .register_routes import register_all_routes

# create fastapi app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://milk-mart-admin-panel.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect db & tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    auto_sync_schema()
    seed_superadmin()

# connect all routes here
app.include_router(register_all_routes)