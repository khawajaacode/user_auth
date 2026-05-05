from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.otp import router as otp_router
from app.routes.profile import router as profile_router
from app.routes.feed import router as feed_router
from app.services.seed_service import seed_feeds

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_feeds()
    yield

app = FastAPI(title="User Auth API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(otp_router)
app.include_router(profile_router)
app.include_router(feed_router)

@app.get("/")
async def root():
    return {"status": "running"}