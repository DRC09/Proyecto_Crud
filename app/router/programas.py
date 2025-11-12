from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.crud.programas import get_program_by_code, update_url_pdf
from app.utils.utils import save_uploaded_document
from core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/programas",
    tags=["Documentos"]
)

@router.post("/upload/")
def upload_document(
    codigo: int, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    """
    Sube un archivo PDF, Word o Excel al servidor y devuelve su ruta de almacenamiento.
    """
    try:
        #Filtro para que primero busque el programa
        file_path = save_uploaded_document(file)
        programa=get_program_by_code(db, codigo)

        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

        save_url= update_url_pdf(db, codigo, file_path)

        return {
            "message": "Archivo subido correctamente",
            "filename": file.filename,
            "ruta_servidor": file_path
        }
    except HTTPException as e:
        # Retorna los errores personalizados definidos en la función
        raise e
    except Exception as e:
        # Captura cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
