"""Local S3-AC11 reads scoped to one current manager assignment."""
from fastapi import APIRouter, HTTPException, Request, Response

from app import models
from app.requests import RequestResponse, _database_id

router = APIRouter()


@router.get("/manager/communities/{community_id}/requests", response_model=list[RequestResponse])
def list_manager_requests(community_id: str, request: Request, response: Response):
    response.headers["Cache-Control"] = "no-store"
    with models.connection() as conn:
        user_id = _database_id(request.headers.get("X-User-Id"))
        if user_id is None or not models.user_exists(conn, user_id):
            raise HTTPException(401, "Unknown user", headers={"Cache-Control": "no-store"})
        selected = _database_id(community_id)
        if selected is None:
            raise HTTPException(404, "Not found", headers={"Cache-Control": "no-store"})
        # Lock the assignment independently of request rows, including empty
        # communities. FOR SHARE also blocks non-key role changes, unlike KEY SHARE.
        membership = conn.execute(
            """SELECT 1 FROM memberships
               WHERE user_id = %s AND community_id = %s AND role = 'manager'
               FOR SHARE""",
            (user_id, selected),
        ).fetchone()
        if membership is None:
            raise HTTPException(404, "Not found", headers={"Cache-Control": "no-store"})
        rows = conn.execute(
            """SELECT id, community_id, unit_id, category, description, status, created_at
               FROM maintenance_requests WHERE community_id = %s
               ORDER BY created_at DESC, id DESC""",
            (selected,),
        ).fetchall()
        # Validate every row before leaving the transaction and releasing its lock.
        return [RequestResponse.model_validate(row) for row in rows]
