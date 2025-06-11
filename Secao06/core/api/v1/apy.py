from fastapi import APIRouter
from core.api.v1.endpoints import usuario, artigo


api = APIRouter()

api.include_router(
    usuario.router,
    prefix="/usuarios",
    tags=["usuarios"]
)
api.include_router(
    artigo.router,
    prefix="/artigos",
    tags=["artigos"]
)