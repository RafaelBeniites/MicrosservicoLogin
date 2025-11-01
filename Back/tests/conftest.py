from collections.abc import AsyncIterator, Iterator
import sys
from pathlib import Path

from sqlalchemy.pool import StaticPool

SERVICE_PATH = Path(__file__).resolve().parents[1]
if str(SERVICE_PATH) not in sys.path:
    sys.path.insert(0, str(SERVICE_PATH))

for module_name in list(sys.modules):
    if module_name == "app" or module_name.startswith("app."):
        sys.modules.pop(module_name)

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import create_app
from app.db import session as db_session
from app.models import token, user  # noqa: F401


@pytest.fixture(scope="module")
def engine():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db_session.engine = test_engine
    SQLModel.metadata.create_all(test_engine)
    return test_engine


@pytest.fixture(scope="module")
def app(engine):
    test_app = create_app()

    SQLModel.metadata.create_all(engine)

    def override_get_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    test_app.dependency_overrides[db_session.get_session] = override_get_session
    return test_app


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client
