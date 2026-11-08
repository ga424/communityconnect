"""Local S3-AC12 options; each read uses current manager memberships."""
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from app import models
from app.requests import _database_id

router = APIRouter()


class CommunityOption(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)


@router.get("/manager/communities", response_model=list[CommunityOption])
def list_manager_communities(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-store"
    with models.connection() as conn:
        user_id = _database_id(request.headers.get("X-User-Id"))
        if user_id is None or not models.user_exists(conn, user_id):
            raise HTTPException(401, "Unknown user", headers={"Cache-Control": "no-store"})
        rows = conn.execute(
            """SELECT c.id, c.name FROM memberships AS m
               JOIN communities AS c ON c.id = m.community_id
               WHERE m.user_id = %s AND m.role = 'manager'
               ORDER BY c.id ASC""",
            (user_id,),
        ).fetchall()
        return [CommunityOption.model_validate(row) for row in rows]
