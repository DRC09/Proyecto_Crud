from typing import List
from ast import List
from unittest import result
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.router.dependencies import get_current_user
from app.schemas.usuarios import CrearUsuario, Editar_usuario, EditarPass, RetornoUsuario
from core.database import get_db
from app.crud import usuarios as crud_users
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)#DECORADOR
def create_user(
    user: CrearUsuario,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permiso")
        
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-id/{id_usuario}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
def get_by_id(
    id_usuario:int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):    
    try:
        user = crud_users.get_user_by_id(db,id_usuario)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-email/{email}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
def get_by_email(
    email:str,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        user = crud_users.get_user_by_email(db,email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/editar/{user_id}")
def update_user(
    user_id: int,
    user: Editar_usuario, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permiso")
        
        success = crud_users.update_user(db, user_id, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/eliminar/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id_usuario: int, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permiso")
        
        user = crud_users.user_delete(db, id_usuario)

        if user:
            return {"message": "Usuario eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/editar-contrasena")
def update_password(
    user: EditarPass, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permiso")
        
        verificar= crud_users.verify_user_pass(db,user)
        if not verificar:
            raise HTTPException(status_code=400, detail="La contraseña actual no es igual")

        success = crud_users.update_password(db, user, EditarPass)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la contraseña")
        return {"message": "Contraseña actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/obtener-todos}", status_code=status.HTTP_200_OK, response_model=List[RetornoUsuario])
def get_all(db: Session = Depends(get_db)):
    try:
        users = crud_users.get_all_user(db)
        if users is None:
            raise HTTPException(status_code=404, detail="Usuarios no encontrados")
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/obtener-todos-secure", status_code=status.HTTP_200_OK, response_model=List[RetornoUsuario])
def get_all_s(
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        users = crud_users.get_all_user(db)
        if users is None:
            raise HTTPException(status_code=404, detail="Usuarios no encontrados")
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))