from fastapi import APIRouter, status
from app.schemas.feed import FeedResponse
from app.services.feed_service import get_all_feeds, get_feed_by_id

router = APIRouter(prefix="/api/v1/feed", tags=["Feed"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[FeedResponse]
)
async def all_feeds():
    return await get_all_feeds()


@router.get(
    "/{feed_id}",
    status_code=status.HTTP_200_OK,
    response_model=FeedResponse
)
async def feed_detail(feed_id: str):
    return await get_feed_by_id(feed_id)