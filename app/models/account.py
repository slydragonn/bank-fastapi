from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    """
    Esquema para crear una nueva cuenta.
    
    Attributes:
      name: Nombre completo del titular de la cuenta (2-100 caracteres)
      email: Dirección de correo electrónico válida para la cuenta
      balance: Saldo inicial de la cuenta (por defecto 0 si no se indica).
    """
    name: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@example.com")
    balance: Optional[float] = Field(
        default=0.0,
        ge=0,
        description="Saldo inicial de la cuenta",
        example=100.50
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "María García",
                "email": "maria.garcia@example.com",
                "balance": 500.75
            }
        }

class AccountOut(BaseModel):
    """
    Esquema completo de la información de la cuenta.
    
    Attributes:
      id: Identificador único de la cuenta
      name: Nombre del titular de la cuenta
      email: Dirección de correo electrónico registrada
      balance: Saldo actual de la cuenta
      created_at: Fecha de creación de la cuenta
    """
    id: str = Field(..., example="507f1f77bcf86cd799439011")
    name: str
    email: EmailStr
    balance: float
    created_at: datetime = Field(default_factory=datetime.now)

class AccountOutId(BaseModel):
    """
    Respuesta de cuenta mínima que sólo contiene el ID.
    
    Attributes:
        id: Identificador único de cuenta
    """
    id: str = Field(..., example="507f1f77bcf86cd799439011")