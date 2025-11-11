from pydantic import BaseSettings
class Settings(BaseSettings):
    K_MIN: int = 2
    K_MAX: int = 10
    MIN_SIZE: int = 5
    MAX_SIZE: int | None = None
    RANDOM_STATE: int = 42
settings = Settings()
