from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from models.usuario_model import UsuarioModel
from core.config import settings
from core.security import verificar_senha

from pydantic import EmailStr

oauth22_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login",
    )

async def autenticar(email: str, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        if not usuario:
            return None
        
        if not verificar_senha(senha, usuario.senha):
            return None
        return usuario
    
def criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    
    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = sub
    
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io/
    """
    return criar_token(
        tipo_token="acess",
        tempo_vida=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
        )