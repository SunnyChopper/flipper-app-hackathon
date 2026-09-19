from fastapi import APIRouter

from app.models.search import SavedSearch, SavedSearchCreate
from app.services.store import deal_store

router = APIRouter(prefix="/api/searches", tags=["searches"])


@router.get("", response_model=list[SavedSearch])
def list_searches() -> list[SavedSearch]:
    return deal_store.list_searches()


@router.post("", response_model=SavedSearch)
def create_search(payload: SavedSearchCreate) -> SavedSearch:
    return deal_store.save_search(payload)
