from models.account import AccountCreate, AccountOut
from datetime import datetime

class AccountService:
  def __init__(self, repository):
    self.repo = repository

  def create_account(self, account_data: AccountCreate) -> AccountOut:
        """
        Crea una nueva cuenta de banco validando los datos
        
        Args:
            account_data: Datos necesarios para crear la cuenta
            
        Returns:
            AccountOut: La cuenta creada con todos los detalles
            
        Raises:
            ValueError: Si la validación falla
        """
        try:
            account_dict = account_data.model_dump()

            # Validación de datos
            if account_data.balance < 0:
                raise ValueError("Initial balance cannot be negative")
            elif account_data.balance == None:
                account_dict["balance"] = 0
            
            # Agregar fecha de creación
            account_dict["created_at"] = datetime.now()
            
            # Crear en la base de datos
            return self.repo.create(account_dict)
            
        except Exception as e:
            print(f"Error al crear cuenta: {str(e)}")
            raise