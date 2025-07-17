from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
from models.account import AccountCreate, AccountOut
from bson import ObjectId
from typing import Optional

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
                balance=account_dict["balance"],
                created_at=account_dict.get("created_at")
            )
            
        except PyMongoError as e:
            print(f"Error en la Base de datos creando la cuenta: {str(e)}")
            raise ValueError("No se pudo crear la cuenta") from e
        
  def _map_to_account_out(self, account_dict: dict) -> AccountOut:
        """Helper para convertir diccionario de la DB al modelo AccountOut"""
        return AccountOut(
            id=str(account_dict["_id"]),
            name=account_dict["name"],
            balance=account_dict["balance"],
            created_at=account_dict.get("created_at")
        )

  def get_all(self) -> list[AccountOut]:
        """
        Obtiene todas las cuentas de bancos

        Returns:
            list[AccountOut]: La lista con los detalles de la cuentas bancarias
        """

        try:
            accounts = self.collection.find()

            return [self._map_to_account_out(acc) for acc in accounts]
        except PyMongoError as e:
            print(f"Error al consultar cuentas en la base de datos: {str(e)}")
            raise

  def get_one_by_id(self, account_id: str) -> AccountOut:
      """
      Obtiene los datos de una cuenta por id

      Args:
        account_id: id de la cuenta de banco

      Returns:
        AccountOut: Todos los detalles de la cuenta 
      """
      try:
          account = self.collection.find_one({"_id": ObjectId(account_id)})

          return self._map_to_account_out(account)
      except PyMongoError as e:
          print(f"Error al consultar la cuenta en la base de datos: {str(e)}")
          raise
      
  def update_balance(self, account_id: str, amount: float) -> Optional[AccountOut]:
      """
        Actualiza el saldo de la cuenta por un monto relativo.
        
        Args:
            account_id: El ID de la cuenta a actualizar
            amount: Monto a añadir (positivo o negativo)
                        
        Returns:
            Cuenta actualizada o None si no se encuentra
            
        Raises:
            ValueError: Si el formato del ID de cuenta no es válido
      """
      try:
          updated_account = self.collection.find_one_and_update(
              {"_id": ObjectId(account_id)},
              {"$set": {"balance": amount}},
              return_document=ReturnDocument.AFTER
          )

          return self._map_to_account_out(updated_account) if updated_account else None
      except PyMongoError as e:
          print(f"Error al actualizar balance en la base de datos: {str(e)}")
          raise ValueError("ID de cuenta u operación de actualización no válidas")
      
  def delete(self, account_id: str):
      """
      Elimina una cuenta por id

      Args:
        account_id: id de la cuenta de banco
      """
      try:
          self.collection.delete_one({"_id": ObjectId(account_id)})
      except PyMongoError as e:
          print(f"Error al eliminar cuenta: {str(e)}")
          raise