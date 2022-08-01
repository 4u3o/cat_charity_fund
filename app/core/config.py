from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд (0.1.0)'
    description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    authentication_backend: str = 'jwt'
    secret: str = 'SECRET'
    min_password_length: int = 3

    class Config:
        env_file = '.env'


settings = Settings()
