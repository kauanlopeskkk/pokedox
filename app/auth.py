import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import API_PASSWORD, API_USERNAME

security = HTTPBasic()


def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    usuario_correto = secrets.compare_digest(credentials.username, API_USERNAME)
    senha_correta = secrets.compare_digest(credentials.password, API_PASSWORD)
    if not (usuario_correto and senha_correta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
