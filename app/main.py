from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.api.v1.anime import router
from app.database.session import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI(title="AniWatch Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api/v1")
