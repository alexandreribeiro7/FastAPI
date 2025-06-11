from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate, UsuarioSchemaArtigos
from core.deps import get_session, get_current_user
from core.security import hash_password_create
from core.auth import criar_token_acesso, autenticar


router = APIRouter()


# Get Logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_usuario_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# Post / Signup / usuario
@router.post("/signup", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(
    usuario: UsuarioSchemaCreate,
    db: AsyncSession = Depends(get_session)
):
    # Verifica se já existe usuário com o mesmo e-mail
    query = select(UsuarioModel).filter(UsuarioModel.email == usuario.email)
    result = await db.execute(query)
    usuario_existente = result.scalars().first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )

    novo_usuario = UsuarioModel(
        name=usuario.name,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=hash_password_create(usuario.senha),
        eh_admin=usuario.eh_admin,
    )
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario

# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(
    db: AsyncSession = Depends(get_session)
):
    query = select(UsuarioModel)
    result = await db.execute(query)
    usuarios: List[UsuarioModel] = result.scalars().unique().all()
    return usuarios
    

# Get Usuario by ID
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=200)
async def get_usuario_by_id(
    usuario_id: int,
    db: AsyncSession = Depends(get_session)
):
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return usuario

# Put Usuario by ID
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=202)
async def put_usuario_by_id(
    usuario_id: int,
    usuario: UsuarioSchemaUpdate,
    db: AsyncSession = Depends(get_session)
):
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuario_update: UsuarioSchemaBase = result.scalars().unique().one_or_none()
    if usuario_update:
        if usuario.name is not None:
            usuario_update.name = usuario.name
        if usuario.sobrenome is not None:
            usuario_update.sobrenome = usuario.sobrenome
        if usuario.email is not None:
            usuario_update.email = usuario.email
        if usuario.senha is not None:
            usuario_update.senha = hash_password_create(usuario.senha)
        if usuario.eh_admin is not None:
            usuario_update.eh_admin = usuario.eh_admin
        await db.commit()
        return usuario_update
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

# Delete Usuario by ID
@router.delete("/{usuario_id}", status_code=204)
async def delete_usuario_by_id(
    usuario_id: int,
    db: AsyncSession = Depends(get_session)
):
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuari_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
    if usuari_del:
        await db.delete(usuari_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

# Login Usuario
@router.post("/login", response_model=Any, status_code=status.HTTP_200_OK)
async def login_usuario(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    usuario = await autenticar(form_data.username, form_data.password, db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha inválidos."
        )

    return JSONResponse(
        content={
            "access_token": criar_token_acesso(sub=usuario.id),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK
    )