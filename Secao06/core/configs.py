from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://admin:alex3245@localhost:5432/faculdade"
    DBBaseModel: ClassVar = Base
    
    JWT_SECRET_KEY: str = 'cFrprAxAVdlNkU2rO7aCRT0akuM7fESH0Lf38PsZLZk'
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # 60 minutes * 24 hours * 7 days => 1 week
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    PROJECT_NAME: str = "Faculdade API"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings: Settings = Settings()