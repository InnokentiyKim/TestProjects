from pydantic.v1 import root_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @root_validator
    def get_database_url(cls, val):
        val['DATABASE_URL'] = (f"postgresql+asyncpg://{val['DB_USER']}:{val['DB_PASSWORD']}"
                               f"@{val['DB_HOST']}:{val['DB_PORT']}/{val['DB_NAME']}")
        return val

    class Config:
        env_file = ".env"

settings = Settings()
print(settings.DB_HOST)