from app.models.feed import Feed
from app.schemas.feed import FeedResponse


async def get_all_feeds() -> list[FeedResponse]:
    feeds = await Feed.find_all().to_list()
    return [
        FeedResponse(
            id=str(feed.id),
            title=feed.title,
            description=feed.description,
            category=feed.category,
            image_url=feed.image_url,
            created_at=feed.created_at
        )
        for feed in feeds
    ]


async def get_feed_by_id(feed_id: str) -> FeedResponse:
    from bson import ObjectId
    from fastapi import HTTPException, status

    try:
        feed = await Feed.get(ObjectId(feed_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )

    return FeedResponse(
        id=str(feed.id),
        title=feed.title,
        description=feed.description,
        category=feed.category,
        image_url=feed.image_url,
        created_at=feed.created_at
    )