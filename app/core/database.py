from pymongo import MongoClient
import os

client = None
db = None

def connect_to_mongo():
  print("Connecting to MongoDB...")
  global client, db
  MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
  client = MongoClient(MONGO_URI)
  db = client["bank_accounts"]
  print("Database conected")


def close_mongo_connection():
  if client:
    print("Closing database...")
    client.close()
    print("Datasebase closed")


def get_database():
  return db