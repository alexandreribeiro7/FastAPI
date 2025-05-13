from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True     #  type : ignore
Select.inherit_cache = True     #  type : ignore
# Fim Bypass


router = APIRouter()

# Post Curso
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def create_curso(curso: CursoModel, db:AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso

# Get Curso
@router.get("/", response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        
        return cursos
    
# Get Curso by ID
@router.get("/{id}", response_model=CursoModel)
async def get_curso_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()
        
        if not curso:
            response.status_code = status.HTTP_404_NOT_FOUND
            return{"detail": f"Curso com id {id} não encontrado"}
        
        return curso
    
# Put Curso
@router.put("/{id}", response_model=CursoModel)
async def put_curso(id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso_up: CursoModel = result.scalar_one_or_none()
        
        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            
            await session.commit()
            
            return curso_up
        
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return{"detail": f"Curso com id {id} não encontrado"}
        
# Delete Curso
@router.delete("/{id}")
async def delete_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso_del: CursoModel = result.scalar_one_or_none()
        
        if curso_del:
            await session.delete(curso_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_200_OK)
        
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return{"detail": f"Curso com id {id} não encontrado"}