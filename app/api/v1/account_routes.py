from fastapi import APIRouter, Depends, status
from app.core.database import get_database
from app.models.account import AccountCreate, AccountOutId, AccountOut, BalanceAdjustment, BalanceOut
from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService

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
    - **balance**: float (optional, default=0) - Saldo inicial de la cuenta

    ## Response
    Devuelve el ObjectId de MongoDB de la cuenta recién creada

    ## Ejemplo de solicitud
    ```json
    {
        "name": "Juan Pérez",
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
            "balance": 0,
            "created_at": "2025-07-17T20:39:08.439000"
        }
    ]
    """
   
   accounts_list = service.get_all_accounts()

   return accounts_list

@router.get("/{account_id}", response_model=AccountOut, tags=["Accounts"])
async def get_account(account_id: str, service: AccountService = Depends(get_service)) -> AccountOut:
   """
    Devuelve una cuenta de banco.

    ## Ejemplo de respuesta
    ```json
    {
        "id": "68795f6c6651bb3bbb6719ab",
        "name": "Juan Pérez",
        "balance": 0,
        "created_at": "2025-07-17T20:39:08.439000"
    }
    """
   account = service.get_account_by_id(account_id)

   return account


@router.patch(
   "/{account_id}",
   response_model=BalanceOut,
   tags=["Accounts"],
   responses={
        200: {"description": "Balance adjusted successfully"},
        404: {
            "description": "Account not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Account not found"}
                }
            }
        }
    }
)
async def update_balance(
   account_id: str,
   adjustment: BalanceAdjustment,
   service: AccountService = Depends(get_service)
) -> BalanceOut:
   """
   Ajusta el saldo de la cuenta con el monto especificado.
    
    - Los importes positivos aumentan el saldo
    - Los importes negativos disminuyen el saldo
   """
   return service.update_account_balance(account_id, adjustment.amount)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Accounts"])
async def delete_account(account_id: str, service: AccountService = Depends(get_service)):
   """
    Elimina una cuenta de banco.
   """
   return service.delete_account(account_id)