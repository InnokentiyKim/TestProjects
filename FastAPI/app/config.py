from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str 
    DB_PASSWORD: str 
    DB_NAME: str 
    
    class Config:
        env_file = ".env"
        
    @property
    def DSN(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        

settings = Settings()

