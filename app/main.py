from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.logger import setup_logger
from app.users.routes import router as user_router
from app.trackers.water_tracker.routes import router as water_router
from app.trackers.meals_tracker.routes import router as meal_router
from app.trackers.bmi_tracker.routes import router as bmi_router
from app.trackers.sleep_tracker.routes import router as sleep_router
from app.trackers.mood_tracker.routes import router as mood_router
from app.trackers.medication_tracker.routes import router as medication_router
from app.daily_summary.routes import router as daily_summary_router
from app.startup import load_all_schemas

setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_all_schemas()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(water_router)
app.include_router(meal_router)
app.include_router(bmi_router)
app.include_router(sleep_router)
app.include_router(mood_router)
app.include_router(medication_router)
app.include_router(daily_summary_router)