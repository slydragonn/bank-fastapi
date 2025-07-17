from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup
  connect_to_mongo()

  yield

  # Shotdown
  close_mongo_connection()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
  return {"message": "Hello World!"}