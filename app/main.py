from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.users.routes import router as user_router
from app.trackers.water_tracker.routes import router as water_router
from app.trackers.meals_tracker.routes import router as meal_router
from app.trackers.bmi_tracker.routes import router as bmi_router
from app.startup import load_all_schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_all_schemas()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(water_router)
app.include_router(meal_router)
app.include_router(bmi_router)