from pymongo import MongoClient
import os

client = None
db = None

def connect_to_mongo():
  print("Conectando a MongoDB...")
  global client, db
  MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
  IS_TESTING = os.getenv("TESTING", "0") == "1"
  client = MongoClient(MONGO_URI)
  db = client["test_db"] if IS_TESTING else client["bank_accounts"]
  print("Base de datos conectada")


def close_mongo_connection():
  if client:
    print("Cerrando base de datos...")
    client.close()
    print("Base de datos cerrada correctamente")


def get_database():
  return db