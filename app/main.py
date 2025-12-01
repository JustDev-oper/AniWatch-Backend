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

# Serve uploaded files when running locally. When using S3 this still works
# for any existing local files.
# Ensure static directory exists before mounting — Starlette/StaticFiles raises a
# RuntimeError when the directory does not exist. Use the current working
# directory so local dev and tests behave the same as save_image_locally.
STATIC_DIR = os.path.abspath(os.path.join(os.getcwd(), 'static'))
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
