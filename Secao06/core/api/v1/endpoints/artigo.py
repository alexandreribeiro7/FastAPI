from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_models import ArtigoModel
from models.usuario_model import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.artigo_schema import ArtigoSchema

router = APIRouter()

# post artigo

@router.post("/", response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=usuario_logado.id
    )
    db.add(novo_artigo)
    await db.commit()

    return novo_artigo

# get artigos

@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(
    db: AsyncSession = Depends(get_session)
):
    async with db() as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        return artigos
    
# get artigo by id

@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=200)
async def get_artigo_by_id(
    artigo_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db() as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado."
            )
        
        return artigo
    
#Put artigo by id]
   
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=202)
async def put_artigo_by_id(
    artigo_id: int,
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)
):
    async with db() as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo_up:
            if artigo.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_up.url_fonte = artigo.url_fonte
                if usuario_logado.id != artigo_up.usuario_id:
                    artigo_up.usuario_id = usuario_logado.id
            await session.commit()
            return artigo_up
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado."
            )
        
# Delete artigo by id

@router.delete("/{artigo_id}", status_code=204)
async def delete_artigo_by_id(
    artigo_id: int,
    db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)
):
    async with db() as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo_del:
            if usuario_logado.id != artigo_del.usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você não tem permissão para deletar este artigo."
                )
            await session.delete(artigo_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado."
            )