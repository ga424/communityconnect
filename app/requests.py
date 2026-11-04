"""Explicit S-1 stubs. Implement only after the bounded task is approved."""
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/communities/{community_id}/requests")
def create_request(community_id: str):
    raise HTTPException(501, "S-1 implementation pending approval")


@router.get("/communities/{community_id}/requests")
def list_requests(community_id: str):
    raise HTTPException(501, "S-1 implementation pending approval")


@router.get("/requests/{request_id}")
def get_request(request_id: str):
    raise HTTPException(501, "S-1 implementation pending approval")
