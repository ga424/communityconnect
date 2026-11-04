"""AC-1 local resident create/list contract; request details remain deferred."""
from datetime import datetime, timezone
import json
import re
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, ValidationError, field_serializer
from starlette.concurrency import run_in_threadpool

from app import clock, models, settings

router = APIRouter()


class CreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    category: str
    description: str


class RequestResponse(BaseModel):
    id: int
    community_id: int
    unit_id: int
    category: str
    description: str
    status: Literal["Open", "In progress", "Resolved"]
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _database_id(value: str | None) -> int | None:
    # IDs are ASCII positive decimals stored in PostgreSQL INTEGER columns.
    # Avoid converting arbitrary-length input or sending overflow values to SQL.
    if value is None or len(value) > 10 or re.fullmatch(r"[1-9][0-9]*", value) is None:
        return None
    result = int(value)
    return result if result <= 2_147_483_647 else None


def _resident(conn, caller: str | None, community: str) -> tuple[int, int, int]:
    user_id = _database_id(caller)
    if user_id is None or not models.user_exists(conn, user_id):
        raise HTTPException(401, "Unknown user")
    community_id = _database_id(community)
    if community_id is None:
        raise HTTPException(404, "Not found")
    unit_id = models.resident_unit(conn, user_id, community_id)
    if unit_id is None:
        raise HTTPException(404, "Not found")
    return user_id, community_id, unit_id


def _create_request(caller: str | None, community: str, raw_body: bytes) -> RequestResponse:
    # One transaction spans authorization, validation and the single insert.
    with models.connection() as conn:
        user_id, community_id, unit_id = _resident(conn, caller, community)
        try:
            body = CreateRequest.model_validate(json.loads(raw_body))
        except (ValueError, UnicodeDecodeError, ValidationError):
            raise HTTPException(422, "Invalid request body") from None
        description = body.description.strip()
        if not description:
            raise HTTPException(422, "Description is required")
        if len(description) > settings.MAX_DESCRIPTION_CHARS:
            raise HTTPException(422, "Description is too long")
        if body.category not in settings.REQUEST_CATEGORIES:
            raise HTTPException(422, "Unknown category")
        row = models.insert_request(
            conn, user_id=user_id, community_id=community_id, unit_id=unit_id,
            category=body.category, description=description, created_at=clock.now(),
        )
        result = RequestResponse.model_validate(row)
    return result


@router.post("/communities/{community_id}/requests", status_code=201, response_model=RequestResponse)
async def create_request(community_id: str, request: Request):
    # Raw bytes defer JSON validation until after identity and membership checks.
    raw_body = await request.body()
    return await run_in_threadpool(
        _create_request, request.headers.get("X-User-Id"), community_id, raw_body,
    )


@router.get("/communities/{community_id}/requests", response_model=list[RequestResponse])
def list_requests(community_id: str, request: Request):
    with models.connection() as conn:
        user_id, resolved_community, _ = _resident(conn, request.headers.get("X-User-Id"), community_id)
        return [RequestResponse.model_validate(row) for row in models.own_requests(
            conn, user_id=user_id, community_id=resolved_community,
        )]


@router.get("/requests/{request_id}")
def get_request(request_id: str):
    raise HTTPException(501, "S-1 implementation pending approval")
