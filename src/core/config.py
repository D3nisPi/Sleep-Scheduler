from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str
    port: int


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class EngineConfig(BaseModel):
    echo: bool
    pool_size: int
    max_overflow: int


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expiration_minutes: int
    refresh_token_expiration_days: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter=".",
        env_prefix="app.",
    )
    run: RunConfig
    db: DatabaseConfig
    engine: EngineConfig
    jwt: JWTConfig


settings = Settings()
