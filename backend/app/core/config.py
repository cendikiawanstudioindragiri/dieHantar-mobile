from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json


class Settings(BaseSettings):
    # Core
    DATABASE_URL: str = "mysql+pymysql://root:example@mysql:3306/diehantar_db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment / ops
    ENV: str = "development"  # development|staging|production
    LOG_LEVEL: str = "info"    # info|debug|warning|error

    # Integration / async
    REDIS_URL: str | None = None
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None

    # Feature flags (direct dict) & optional JSON source
    FEATURE_FLAGS: dict[str, bool] = {}
    FEATURE_FLAGS_JSON: str | None = None  # if provided, overrides FEATURE_FLAGS

    # Security policies
    PASSWORD_MIN_LENGTH: int = 6
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_SECONDS: int = 300

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v: str):
        if v == "change-me" or len(v) < 32:
            # Fail fast in production; allow shorter in dev but warn.
            raise ValueError("SECRET_KEY too weak. Provide a random string >=32 chars.")
        return v

    @field_validator("ENV")
    def normalize_env(cls, v: str):
        v_lower = v.lower()
        if v_lower not in {"development", "staging", "production", "test"}:
            raise ValueError("ENV must be one of development|staging|production|test")
        return v_lower

    @field_validator("LOG_LEVEL")
    def normalize_log_level(cls, v: str):
        v_lower = v.lower()
        if v_lower not in {"debug", "info", "warning", "error", "critical"}:
            raise ValueError("LOG_LEVEL invalid")
        return v_lower

    @field_validator("FEATURE_FLAGS_JSON")
    def parse_feature_flags_json(cls, v: str | None, info):
        if not v:
            return v
        try:
            data = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid FEATURE_FLAGS_JSON: {e}")
        if not isinstance(data, dict):
            raise ValueError("FEATURE_FLAGS_JSON must decode to an object")
        # Coerce values to bool
        for k, val in data.items():
            data[k] = bool(val)
        # override FEATURE_FLAGS field if JSON provided
        info.data.get("FEATURE_FLAGS", {}).update(data)
        return v

    @field_validator("PASSWORD_MIN_LENGTH")
    def password_min_length_positive(cls, v: int):
        if v < 6:
            raise ValueError("PASSWORD_MIN_LENGTH must be >= 6")
        return v

    @field_validator("MAX_LOGIN_ATTEMPTS")
    def max_login_attempts_positive(cls, v: int):
        if v < 1:
            raise ValueError("MAX_LOGIN_ATTEMPTS must be >= 1")
        return v

    @field_validator("LOGIN_LOCKOUT_SECONDS")
    def login_lockout_seconds_positive(cls, v: int):
        if v < 1:
            raise ValueError("LOGIN_LOCKOUT_SECONDS must be >= 1")
        return v


settings = Settings()  # reads from environment/.env
