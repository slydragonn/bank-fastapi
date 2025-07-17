from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import connect_to_mongo, close_mongo_connection
from api.v1 import account_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
  """
  Context manager para manejar el ciclo de vida de la aplicación FastAPI.
  
  Se encarga de:
  - Inicializar conexiones y recursos al iniciar
  - Limpiar recursos al finalizar
  
  Args:
      app: Instancia de FastAPI
      
  Yields:
      Control a la aplicación manteniendo los recursos activos
  """
  
  # Startup
  try:
    connect_to_mongo()  # Establece conexión con MongoDB
    print("Conexión a MongoDB establecida correctamente")
  except Exception as e:
    print(f"Error al conectar a MongoDB: {str(e)}")
    raise

  yield

  # Shutdown
  try:
    close_mongo_connection()  # Cierra conexión limpiamente
    print("Conexión a MongoDB cerrada correctamente")
  except Exception as e:
    print(f"Error al cerrar conexión MongoDB: {str(e)}")

# Configuración principal de FastAPI
app = FastAPI(
  lifespan=lifespan,
  title="Bank API",
  version="1.0.0",
  description="API para gestión de cuentas bancarias",
)

# Incluye el router de las cuentas
app.include_router(account_routes.router, prefix="/api/v1/accounts", tags=["Accounts"])