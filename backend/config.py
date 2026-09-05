from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ProofPay"
    auto_submit_amount_limit_inr: float = 150_000
    minimum_confidence: float = 0.80
    model_name: str = "gpt-4o-mini"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_prefix="SENTINEL_", env_file=".env", extra="ignore", protected_namespaces=())


settings = Settings()
