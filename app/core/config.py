from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = (
        'Благотворительный фонд поддержки котиков QRKot '
        'собирает пожертвования на различные целевые проекты.'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    authentication_backend: str = 'jwt'
    secret: str = 'SECRET'
    min_password_length: int = 3
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


    class Config:
        env_file = '.env'


settings = Settings()
