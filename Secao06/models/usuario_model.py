from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    sobrenome = Column(String(256))
    email = Column(String(256), unique=True, index=True, nullable=False)
    senha = Column(String(256), nullable=False)
    eh_admin = Column(Boolean, default=False)
    artigos = relationship("ArtigoModel", back_populates="criador", cascade="all,delete-orphan", uselist=True, lazy="joined")