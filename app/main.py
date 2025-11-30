from fastapi import FastAPI

app: FastAPI = FastAPI(title="AniWatch Backend", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to AniWatch Backend"}

# Include API routes
# from app.api import router as api_router
# app.include_router(api_router, prefix="/api/v1")