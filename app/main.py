from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.anime import router
from app.database.session import Base, engine

app: FastAPI = FastAPI(title="AniWatch Backend")

Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api/v1")

# Serve uploaded files when running locally. When using S3 this still works
# for any existing local files.
app.mount('/static', StaticFiles(directory='static'), name='static')
