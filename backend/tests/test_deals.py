from app.data.ids import LISTING_IPHONE_CRACKED


def test_put_deals_creates_user_deal(client):
    response = client.put(
        f"/api/v1/deals/{LISTING_IPHONE_CRACKED}",
        json={"status": "saved", "notes": None},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["listingId"] == LISTING_IPHONE_CRACKED
    assert body["status"] == "saved"
    assert body["id"]
    assert body["createdAt"]
    assert body["updatedAt"]


def test_put_deals_updates_existing_user_deal(client):
    created = client.put(
        f"/api/v1/deals/{LISTING_IPHONE_CRACKED}",
        json={"status": "saved"},
    ).json()
    updated = client.put(
        f"/api/v1/deals/{LISTING_IPHONE_CRACKED}",
        json={"status": "acquired", "notes": "Bought locally"},
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["id"] == created["id"]
    assert body["status"] == "acquired"
    assert body["notes"] == "Bought locally"


def test_get_deals_returns_saved_summaries(client):
    client.put(f"/api/v1/deals/{LISTING_IPHONE_CRACKED}", json={"status": "saved"})
    response = client.get("/api/v1/deals", params={"status": "saved"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    item = body["items"][0]
    assert item["userDeal"]["status"] == "saved"
    assert item["opportunity"]["listingId"] == LISTING_IPHONE_CRACKED
    assert item["opportunity"]["dealScore"] >= 1


def test_delete_deals_removes_saved_state(client):
    client.put(f"/api/v1/deals/{LISTING_IPHONE_CRACKED}", json={"status": "saved"})
    deleted = client.delete(f"/api/v1/deals/{LISTING_IPHONE_CRACKED}")
    assert deleted.status_code == 204
    listed = client.get("/api/v1/deals", params={"status": "saved"})
    assert listed.json()["items"] == []


def test_opportunity_includes_saved_status_after_put(client):
    client.put(f"/api/v1/deals/{LISTING_IPHONE_CRACKED}", json={"status": "saved"})
    detail = client.get(f"/api/v1/opportunities/{LISTING_IPHONE_CRACKED}").json()
    assert detail["userDeal"]["status"] == "saved"
    summary = client.get("/api/v1/opportunities").json()["items"]
    match = next(item for item in summary if item["listingId"] == LISTING_IPHONE_CRACKED)
    assert match["userDealStatus"] == "saved"
