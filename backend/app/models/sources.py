from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SourceModel(BaseModel):
    """Lenient wrapper for third-party payloads. Extra keys are kept off the canonical Listing."""

    model_config = ConfigDict(extra="ignore")


class MoneyAmount(SourceModel):
    value: str | float | None = None
    currency: str | None = None
    amount: str | float | None = None
    formatted_amount: str | None = None


class TextBlob(SourceModel):
    text: str | None = None


class FacebookPhoto(SourceModel):
    uri: str | None = None


class FacebookPrimaryPhoto(SourceModel):
    image: FacebookPhoto | None = None
    uri: str | None = None
    photo_image_url: str | None = None


class FacebookCityPage(SourceModel):
    display_name: str | None = None


class FacebookReverseGeocode(SourceModel):
    city: str | None = None
    state: str | None = None
    city_page: FacebookCityPage | None = None


class FacebookLocation(SourceModel):
    reverse_geocode: FacebookReverseGeocode | None = None
    city: str | None = None
    state: str | None = None


class FacebookSeller(SourceModel):
    name: str | None = None
    id: str | None = None


class FacebookMarketplaceItem(SourceModel):
    """Dataset row from apify/facebook-marketplace-scraper (and close variants)."""

    id: str | int | None = None
    listingUrl: str | None = None
    facebookUrl: str | None = None
    itemUrl: str | None = None
    marketplace_listing_title: str | None = Field(
        default=None,
        validation_alias=AliasChoices("marketplace_listing_title", "listingTitle"),
    )
    title: str | None = None
    custom_title: str | None = None
    listing_price: MoneyAmount | str | float | None = Field(
        default=None,
        validation_alias=AliasChoices("listing_price", "listingPrice"),
    )
    price: MoneyAmount | str | float | None = None
    strikethrough_price: MoneyAmount | None = None
    primary_listing_photo: FacebookPrimaryPhoto | None = None
    listingPhotos: list[FacebookPrimaryPhoto] = Field(default_factory=list)
    location: FacebookLocation | None = None
    locationText: TextBlob | str | None = None
    marketplace_listing_seller: FacebookSeller | None = None
    delivery_types: list[str] = Field(default_factory=list)
    is_hidden: bool = Field(default=False, validation_alias=AliasChoices("is_hidden", "isHidden"))
    is_live: bool | None = Field(default=None, validation_alias=AliasChoices("is_live", "isLive"))
    is_pending: bool = Field(default=False, validation_alias=AliasChoices("is_pending", "isPending"))
    is_sold: bool = Field(default=False, validation_alias=AliasChoices("is_sold", "isSold"))
    description: str | TextBlob | None = None
    redacted_description: str | TextBlob | None = None
    condition: str | None = None
    marketplace_listing_category_id: str | None = None


class EbayImage(SourceModel):
    imageUrl: str | None = None


class EbayItemLocation(SourceModel):
    city: str | None = None
    stateOrProvince: str | None = None
    country: str | None = None
    postalCode: str | None = None


class EbaySeller(SourceModel):
    username: str | None = None
    feedbackPercentage: str | None = None
    feedbackScore: int | None = None


class EbayApifyItem(SourceModel):
    """Dataset row from an eBay Apify actor (datascrapers/ebay-scraper and close variants)."""

    itemId: str | int | None = None
    id: str | int | None = None
    title: str | None = None
    url: str | None = None
    itemUrl: str | None = None
    itemWebUrl: str | None = None
    link: str | None = None
    price: MoneyAmount | str | float | None = None
    currency: str | None = None
    formattedPrice: str | None = None
    condition: str | None = None
    buyingFormat: str | None = None
    shipping: MoneyAmount | str | float | None = None
    shippingCost: MoneyAmount | str | float | None = None
    itemLocation: EbayItemLocation | str | None = None
    location: str | None = None
    imageUrl: str | None = None
    image: EbayImage | str | None = None
    images: list[str] = Field(default_factory=list)
    thumbnail: str | None = None
    seller: EbaySeller | str | None = None
    sellerFeedbackPercent: float | str | None = None
    description: str | None = None
    shortDescription: str | None = None
    isSponsored: bool | None = None
    marketplace: str | None = None
