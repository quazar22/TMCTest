import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from test_api.dependencies import get_db
from test_api.routers.users import router
from test_api.models.user import User

app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def override_get_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def sample_users():
    return [User(
        id=1,
        first_name="John",
        last_name="Doe", 
        age=30,
        date_of_birth=datetime(1994, 12, 17, 10, 30, 0, tzinfo=timezone.utc)
    ), User(
        id=2,
        first_name="Jane",
        last_name="Smith", 
        age=25,
        date_of_birth=datetime(2000, 11, 20, 14, 45, 0, tzinfo=timezone.utc)
    )]

@pytest.fixture
def sample_users_create():
    return [{
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "date_of_birth": "1994-12-17T10:30:00Z"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "age": 25,
        "date_of_birth": "2000-11-20T14:45:00Z"
    }]

class TestGetUsers:
    @patch("test_api.routers.users.get_users_db")
    def test_get_users_success(self, mock_get_users_db, mock_db, sample_users, override_get_db):
        mock_get_users_db.return_value = sample_users

        response = client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2