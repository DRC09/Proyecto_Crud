from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    nombre_completo: str = Field(min_length=3, max_length=80)
    id_rol: int
    correo: EmailStr
    num_documento: str = Field(min_length=3, max_length=12)
    estado: bool


class CrearUsuario(UsuarioBase):
    contra_encript: str = Field(min_length=8)
    estado: bool = True


class RetornoUsuario(UsuarioBase):
    id_usuario: int
    estado: bool
    nombre_rol: str

class Editar_usuario(BaseModel):#CUANDO UNO VA A VOTAR LOS DATOS DEBEN DE SER OPCIONALES
    nombre_completo: Optional[str] = Field(default=None, min_length=3, max_length=80)#DEFAULT NONE ES OBLIGATORIO, SI NO SE PONE AL MANDAR UN DATO VACIO CARGA NULL
    correo: Optional[str] = Field(default=None, min_length=6, max_length=50)
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=15)
    numero_documento: Optional[str] = Field(default=None, min_length=7, max_length=15)
    estado: Optional[bool] = None


class EditarPass(BaseModel): #BaseModel es de pydantic
    id_usuario: int
    contra_anterior: str = Field(min_length=8)
    contra_nueva: str = Field(min_length=8)
