from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="User Auth API", lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"status": "running"}
