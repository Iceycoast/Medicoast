from fastapi import FastAPI
from app.users.routes import router as user_router
from app.users.logic import init_user_table

init_user_table()

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["Users"])