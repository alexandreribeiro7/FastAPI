from typing import Optional
from pydantic import BaseModel, HttpUrl

class ArtigoSchema(BaseModel):
    id: Optional[int]
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[int]

    class Config:
        orm_mode = True

        ## exmplos para o uso do pydantic
        schema_extra = {
            "example": {
                "titulo": "Título do Artigo",
                "descricao": "Descrição do Artigo",
                "url_fonte": "https://www.exemplo.com/artigo",
                "usuario_id": 1
            }
        }