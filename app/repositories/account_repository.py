from pymongo.errors import PyMongoError
from models.account import AccountCreate, AccountOut

class AccountRepository:
  def __init__(self, db):
    self.collection = db["accounts"]

  def create(self, account_dict: AccountCreate) -> AccountOut:
        """
        Crea una nueva cuenta en la base de datos
        
        Args:
            account_dict: Datos de la cuenta validados
            
        Returns:
            AccountOut: La cuenta de banco creada con el ID generado por la base de datos
            
        Raises:
            ValueError: Si los datos de la cuenta son invalidos
        """
        try:
            result = self.collection.insert_one(account_dict)
            
            return AccountOut(
                id=str(result.inserted_id),
                name=account_dict["name"],
                email=account_dict["email"],
                balance=account_dict["balance"],
                created_at=account_dict.get("created_at")
            )
            
        except PyMongoError as e:
            print(f"Error en la Base de datos creando la cuenta: {str(e)}")
            raise ValueError("No se pudo crear la cuenta") from e