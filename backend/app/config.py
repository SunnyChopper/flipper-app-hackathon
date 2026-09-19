from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str = ""
    supabase_service_role_key: str = ""
    ebay_marketplace_id: str = "EBAY_US"
    apify_token: str = ""
    apify_facebook_actor: str = "apify~facebook-marketplace-scraper"
    apify_ebay_actor: str = "datascrapers~ebay-scraper"
    apify_run_timeout_seconds: int = 180
    openai_api_key: str = ""
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)


settings = Settings()
