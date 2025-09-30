from fastapi import FastAPI
from app.api.routers import auth, quiz, community, interview
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(community.router)
app.include_router(interview.router)