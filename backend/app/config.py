from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_BACKEND_ROOT / ".env", Path(".env")),
        extra="ignore",
    )

    supabase_url: str = ""
    supabase_service_role_key: str = ""
    ebay_marketplace_id: str = "EBAY_US"
    apify_token: str = ""
    apify_facebook_actor: str = "apify~facebook-marketplace-scraper"
    apify_ebay_actor: str = "datascrapers~ebay-scraper"
    apify_run_timeout_seconds: int = 180
    apify_max_items: int = 5
    apify_ingest_sources: str = "ebay"
    crawl_enabled: bool = True
    crawl_interval_seconds: int = 60
    crawl_categories: str = "phones,tvs,electronics,other"
    openai_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://localhost:5174"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)

    @property
    def ingest_source_list(self) -> list[str]:
        raw = [part.strip() for part in self.apify_ingest_sources.split(",") if part.strip()]
        return raw or ["ebay"]


settings = Settings()
