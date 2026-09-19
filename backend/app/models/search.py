from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class SavedSearchCreate(BaseModel):
    name: str
    query: str = ""
    filters: dict[str, Any] = Field(default_factory=dict)
    notify: bool = True
    user_id: str = "demo-user"


class SavedSearch(SavedSearchCreate):
    id: str = Field(default_factory=lambda: str(uuid4()))
