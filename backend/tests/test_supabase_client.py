from app.services.supabase_client import get_supabase_client


def test_get_supabase_client_returns_none_without_credentials():
    assert get_supabase_client("", "") is None
    assert get_supabase_client("https://example.supabase.co", "") is None
    assert get_supabase_client("", "service-role-key") is None
