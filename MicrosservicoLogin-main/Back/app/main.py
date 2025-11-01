from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_auth import router as auth_router
from app.core.config import settings
from app.db.session import init_db


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Handles authentication, registration and JWT issuance.",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event("startup")
    def on_startup() -> None:
        init_db()

    application.include_router(auth_router, prefix=settings.api_prefix)

    @application.get("/health", tags=["system"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

