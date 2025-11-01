from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


def _create_engine():
    connect_args = {}
    if settings.sql_database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(settings.sql_database_url, echo=False, connect_args=connect_args)


engine = _create_engine()


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

