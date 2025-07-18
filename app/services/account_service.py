from app.models.account import AccountCreate, AccountOut
from datetime import datetime
from fastapi import HTTPException, status

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

  def get_all_accounts(self) -> list[AccountOut]:
      """
      Lista todas las cuentas de banco

      Returns:
        Lista de cuentas
      """
      try:
          return self.repo.get_all()
      except Exception as e:
          print(f"Error al obtener cuentas: {str(e)}")
          raise
      
  def get_account_by_id(self, account_id: str) -> AccountOut:
      """
      Devuelve los detalles de la cuenta bancaria

      Args:
        account_id: id de la cuenta a consultar
      
      Returns:
        AccountOut: Todos de los detalles de la cuenta
      """

      try:
          return self.repo.get_one_by_id(account_id)
      except Exception as e:
          print(f"Error al obtener la cuenta: {str(e)}")
          raise
      
  def update_account_balance(self, account_id: str, amount: float) -> AccountOut:
      """
      Actualiza el saldo de la cuenta por un monto relativo.
        
      Args:
        account_id: ID de la cuenta a actualizar
        amount: Monto a ajustar (positivo o negativo).
            
      Returns:
        Datos de la cuenta actualizados
      """
      try:
          current_account = self.repo.get_one_by_id(account_id)
          if not current_account:
              raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Cuenta no encontrada"
              )
          
          # Actualizar balance de la cuenta
          updated_balance = current_account.balance + amount
          updated_account = self.repo.update_balance(account_id, updated_balance)
          if not updated_account:
              raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Cuenta no encontrada despues de actualizarse"
              )
          
          return updated_account
      
      except ValueError as e:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=str(e)
          )
      
  def delete_account(self, account_id: str):
      """
      Elimina la cuenta bancaria

      Args:
        account_id: id de la cuenta a consultar
      """
      try:
          self.repo.delete(account_id)
      except Exception as e:
          print(f"Error eliminando la cuenta: {str(e)}")
          raise