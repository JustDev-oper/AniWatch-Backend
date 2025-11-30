from fastapi import FastAPI
from app.api.v1.anime import router
from app.database.session import Base, engine

app: FastAPI = FastAPI(title="AniWatch Backend")

Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api/v1")
