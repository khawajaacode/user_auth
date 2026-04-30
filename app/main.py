from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.otp import router as otp_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="User Auth API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(otp_router)

@app.get("/")
async def root():
    return {"status": "running"}


from app.models.user import User

@app.get("/check-data")
async def check_data():
    users = await User.find_all().to_list()
    return users