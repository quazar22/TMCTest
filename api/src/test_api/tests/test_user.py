import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from test_api.dependencies import get_db
from test_api.routers.user import router
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
def sample_user():
    return User(
        id=1,
        first_name="John",
        last_name="Doe", 
        age=30,
        date_of_birth=datetime(1994, 12, 17, 10, 30, 0, tzinfo=timezone.utc)
    )

@pytest.fixture
def sample_user_create():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "date_of_birth": "1994-12-17T10:30:00Z"
    }

class TestGetUser:
    @patch("test_api.routers.user.get_user_db")
    def test_get_user_success(self, mock_get_user_db, mock_db, sample_user, override_get_db):
        mock_get_user_db.return_value = sample_user

        response = client.get("/user/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

        mock_get_user_db.assert_called_once_with(mock_db, 1)

    @patch("test_api.routers.user.get_user_db", new_callable=AsyncMock)
    def test_get_user_not_found(self, mock_get_user_db, mock_db, override_get_db):
        mock_get_user_db.return_value = None

        response = client.get("/user/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

        mock_get_user_db.assert_awaited_once_with(mock_db, 999)

    @patch('test_api.routers.user.get_user_db')
    @patch('test_api.routers.user.get_db')
    def test_get_user_invalid_id(self, mock_get_user_db, mock_db):
        response = client.get("/user/invalid")
        
        assert response.status_code == 422
        mock_get_user_db.assert_not_called()


class TestCreateUser:
    @patch('test_api.routers.user.create_user_db')
    @patch('test_api.routers.user.get_db')
    def test_create_user_success(self, mock_get_db, mock_create_user_db, mock_db, sample_user, sample_user_create):
        mock_get_db.return_value = mock_db
        mock_create_user_db.return_value = sample_user
        
        response = client.post("/user/", json=sample_user_create)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["age"] == 30
        
        mock_create_user_db.assert_called_once()

    @patch('test_api.routers.user.create_user_db')
    @patch('test_api.routers.user.get_db')
    def test_create_user_failure(self, mock_get_db, mock_create_user_db, mock_db, sample_user_create):
        mock_get_db.return_value = mock_db
        mock_create_user_db.return_value = None
        
        response = client.post("/user/", json=sample_user_create)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "User could not be created"
        
        mock_create_user_db.assert_called_once()

    @patch('test_api.routers.user.create_user_db')
    @patch('test_api.routers.user.get_db')
    def test_create_user_missing_fields(self, mock_get_db, mock_create_user_db, mock_db):
        incomplete_data = {
            "first_name": "John"
        }
        response = client.post("/user/", json=incomplete_data)
        
        assert response.status_code == 422
        
        mock_create_user_db.assert_not_called()

    @patch('test_api.routers.user.create_user_db')
    @patch('test_api.routers.user.get_db')
    def test_create_user_invalid_date_format(self, mock_get_db, mock_create_user_db, mock_db):
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "date_of_birth": "invalid-date-format"
        }
        
        response = client.post("/user/", json=invalid_data)

        assert response.status_code == 422

        mock_create_user_db.assert_not_called()

    @patch('test_api.routers.user.create_user_db')
    @patch('test_api.routers.user.get_db')
    def test_create_user_various_date_formats(self, mock_get_db, mock_create_user_db, mock_db, sample_user):
        mock_get_db.return_value = mock_db
        mock_create_user_db.return_value = sample_user
        
        date_formats = [
            "1993-01-15T10:30:00Z",
            "1993-01-15T10:30:00",
            "1993-01-15T05:30:00-05:00"
        ]
        
        for date_format in date_formats:
            user_data = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "date_of_birth": date_format
            }
            
            response = client.post("/user/", json=user_data)
            assert response.status_code == 200, f"Failed for date format: {date_format}"