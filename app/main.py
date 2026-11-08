import os
from fastapi import FastAPI
from app.requests import router
from app.manager_communities import router as manager_communities_router


def create_app() -> FastAPI:
    if os.environ.get("APP_ENV") != "test":
        raise RuntimeError("This scaffold is local/test-only; set APP_ENV=test")
    app = FastAPI(title="CommunityConnect — local scaffold", docs_url=None, redoc_url=None)
    app.include_router(router)
    app.include_router(manager_communities_router)

    @app.get("/health")
    def health():
        return {"status": "scaffold", "production_eligible": False}

    return app
