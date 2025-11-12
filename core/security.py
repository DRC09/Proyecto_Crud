from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from core.config import settings
import jwt
from jwt import PyJWTError as JWTError

# Configurar hashing de contraseñas

#ESTO ES PARA BCRYPT
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")



# Función para generar un hashed_password
def get_hashed_password(password: str):
    return pwd_context.hash(password)


# Funcion para verificar una contraseña hashada
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#Función para crear un token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

# Función para verificar si un token JWT es valido
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        return int(user_id) if user_id is not None else None
    except jwt.ExpiredSignatureError: # Token ha expirado
        return None
    except JWTError as e:
        return None
