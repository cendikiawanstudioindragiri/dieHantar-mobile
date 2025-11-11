from collections.abc import Generator
from typing import Any

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure strong SECRET_KEY for test settings before app import
os.environ.setdefault("SECRET_KEY", "test-secret-very-long-string-0123456789abcdef0123456789abcd")

from ..main import app
from ..db.session import Base, get_db
# Ensure models are imported so metadata includes all tables
from app.models import (
    user as _user,  # noqa: F401
    category as _category,  # noqa: F401
    product as _product,  # noqa: F401
    location as _location,  # noqa: F401
    order as _order,  # noqa: F401
    order_item as _order_item,  # noqa: F401
    driver as _driver,  # noqa: F401
    payment as _payment,  # noqa: F401
    review as _review,  # noqa: F401
)


# Create a dedicated in-memory SQLite for tests
engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ensure the same in-memory DB persists across sessions
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> Generator[None, None, None]:
    # Create all tables on the test engine
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db() -> Generator[Any, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply dependency override so all routes use the test DB
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db() -> Generator[Any, None, None]:
    """Provides a database session for direct database operations in tests"""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()
