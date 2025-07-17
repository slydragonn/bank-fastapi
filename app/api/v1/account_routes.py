from fastapi import APIRouter, Depends, status
from core.database import get_database
from models.account import AccountCreate, AccountOutId, AccountOut
from repositories.account_repository import AccountRepository
from services.account_service import AccountService

router = APIRouter()

def get_service():
  db = get_database()
  repo = AccountRepository(db)
  return AccountService(repo)

@router.post(
    "/",
    response_model=AccountOutId,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new account",
    response_description="The ID of the newly created account",
    tags=["Accounts"],
    responses={
        201: {
            "description": "Account created successfully",
            "content": {
                "application/json": {
                    "example": {"id": "507f1f77bcf86cd799439011"}
                }
            }
        }
    }
)
async def create_account(
    account: AccountCreate,
    service: AccountService = Depends(get_service)
) -> AccountOutId:
    """
    Crea una nueva cuenta bancaria en el sistema.

    ## Request Body
    - **name**: str (required) - Nombre completo del titular de la cuenta
    - **email**: EmailStr (required) - Dirección de correo electrónico válida para la cuenta
    - **balance**: float (optional, default=0) - Saldo inicial de la cuenta

    ## Response
    Devuelve el ObjectId de MongoDB de la cuenta recién creada

    ## Ejemplo de solicitud
    ```json
    {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "balance": 10000
    }
    ```

    ## Ejemplo de respuesta
    ```json
    {
        "id": "507f1f77bcf86cd799439011"
    }
    """

    data = service.create_account(account).model_dump()
    return {"id": str(data["id"])}


@router.get("/", response_model=list[AccountOut], tags=["Accounts"])
async def get_all_accounts(service: AccountService = Depends(get_service)) -> list[AccountOut]:
   """
    Devuelve la lista de todas las cuentas de banco creadas.

    ## Ejemplo de respuesta
    ```json
    [
        {
            "id": "68795f6c6651bb3bbb6719ab",
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "balance": 0,
            "created_at": "2025-07-17T20:39:08.439000"
        }
    ]
    """
   
   accounts_list = service.get_all_accounts()

   return accounts_list