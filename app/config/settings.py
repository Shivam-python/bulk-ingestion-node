from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str
    HOSPITAL_API_URL: str
    MAX_CONCURRENT_REQUESTS: int = 5
    MAX_UPLOAD_SIZE: int = 51200

    CORS_ALLOW_ORIGINS: str = "*"  # comma-separated
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ALLOW_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ALLOW_ORIGINS.split(",")]


settings = Settings()
