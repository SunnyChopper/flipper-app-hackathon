from app.data.ids import LISTING_IPHONE_CRACKED, LISTING_MBA_PARTS, LISTING_MBA_SCREEN


def test_list_opportunities_returns_valid_dto(client):
    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 1
    assert body["pageSize"] == 20
    assert body["total"] == 6
    assert len(body["items"]) == 6

    item = next(row for row in body["items"] if row["listingId"] == LISTING_IPHONE_CRACKED)
    assert item["source"] == "facebook_marketplace"
    assert item["price"] == 220
    assert item["shippingCost"] == 0
    assert item["condition"] == "damaged"
    assert item["projectedRestorerNet"] == 115
    assert item["estimatedRepairCost"] == 90
    assert item["dealScore"] >= 1
    assert item["userDealStatus"] is None
    assert item["product"]["displayName"] == "Apple iPhone 13 128GB Unlocked"
    assert item["product"]["estimatedWorkingMarketValue"] == 425
    assert item["requiredRepairSkills"] == ["screen_swap"]


def test_list_opportunities_filters_by_min_profit(client):
    response = client.get("/api/v1/opportunities", params={"minProfit": 200})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert {item["listingId"] for item in body["items"]} == {
        LISTING_MBA_PARTS,
        LISTING_MBA_SCREEN,
        "62222222-2222-4222-8222-222222222222",
    }
    assert all(item["projectedRestorerNet"] >= 200 for item in body["items"])


def test_list_opportunities_filters_by_source(client):
    response = client.get("/api/v1/opportunities", params={"source": "facebook_marketplace"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert all(item["source"] == "facebook_marketplace" for item in body["items"])


def test_list_opportunities_sorts_by_profit_desc(client):
    response = client.get("/api/v1/opportunities", params={"sort": "profit_desc"})
    assert response.status_code == 200
    profits = [item["projectedRestorerNet"] for item in response.json()["items"]]
    assert profits == sorted(profits, reverse=True)
    assert response.json()["items"][0]["listingId"] == LISTING_MBA_PARTS


def test_list_opportunities_search_query(client):
    response = client.get("/api/v1/opportunities", params={"q": "iphone"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all("iphone" in item["title"].lower() for item in body["items"])


def test_list_opportunities_paginates(client):
    first = client.get("/api/v1/opportunities", params={"page": 1, "pageSize": 2, "sort": "profit_desc"})
    second = client.get("/api/v1/opportunities", params={"page": 2, "pageSize": 2, "sort": "profit_desc"})
    assert first.status_code == 200
    assert second.status_code == 200
    first_body = first.json()
    second_body = second.json()
    assert first_body["page"] == 1
    assert first_body["pageSize"] == 2
    assert first_body["total"] == 6
    assert len(first_body["items"]) == 2
    assert len(second_body["items"]) == 2
    assert {item["listingId"] for item in first_body["items"]}.isdisjoint(
        {item["listingId"] for item in second_body["items"]}
    )


def test_get_opportunity_joins_product_bom_and_comps(client):
    response = client.get(f"/api/v1/opportunities/{LISTING_IPHONE_CRACKED}")
    assert response.status_code == 200
    body = response.json()

    assert body["listing"]["id"] == LISTING_IPHONE_CRACKED
    assert body["listing"]["externalId"] == "fb-iphone-13-cracked"
    assert body["product"]["displayName"] == "Apple iPhone 13 128GB Unlocked"
    assert body["product"]["estimatedWorkingMarketValue"] == 425

    assert len(body["defects"]) == 1
    defect = body["defects"][0]
    assert defect["componentName"] == "OLED Screen Assembly"
    assert defect["requiredSkillSlug"] == "screen_swap"
    assert defect["avgReplacementCost"] == 90

    assert body["requiredSkills"][0]["slug"] == "screen_swap"
    assert body["requiredSkills"][0]["userHasSkill"] is True

    assert len(body["marketComps"]) == 3
    assert body["marketComps"][0]["totalPrice"] == body["marketComps"][0]["soldPrice"] + body["marketComps"][0]["shippingPrice"]

    financials = body["financials"]
    assert financials["purchasePrice"] == 220
    assert financials["totalReplacementCost"] == 90
    assert financials["totalAcquisitionAndRepairCost"] == 310
    assert financials["projectedRestorerNet"] == 115
    assert financials["roiPercent"] == 37.1

    assert "total" in body["dealScore"]
    assert body["dealScore"]["valuationConfidence"] == 0.92
    assert body["userDeal"] is None


def test_get_opportunity_missing_listing(client):
    response = client.get("/api/v1/opportunities/00000000-0000-4000-8000-999999999999")
    assert response.status_code == 404
