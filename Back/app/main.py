from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.routes_auth import router as auth_router
from app.core.config import settings
from app.db.session import init_db


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Handles authentication, registration and JWT issuance.",
    )

    # --- CORS ---
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Banco de dados ---
    @application.on_event("startup")
    def on_startup() -> None:
        init_db()

    # --- Rotas da API ---
    application.include_router(auth_router, prefix=settings.api_prefix)

    # --- Healthcheck ---
    @application.get("/health", tags=["system"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    # --- Front-end (HTML + static files) ---
    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")

    @application.get("/", response_class=HTMLResponse)
    def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    return application


app = create_app()
