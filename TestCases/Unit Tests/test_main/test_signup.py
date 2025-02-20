from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from bookstore.database import UserCredentials, get_db
from bookstore.main import app
from passlib.context import CryptContext

client=TestClient(app)
pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")
mockDb=MagicMock()
app.dependency_overrides[get_db]=lambda:mockDb

@pytest.fixture
def mockUser():
    return UserCredentials(email='test@abc.com',password=pwd.hash("Test91@"))

    


def test_signupSuccess(mockUser):
    # mockDb.query.return_value.filter.return_value.first.return_value=mockUser
    mockDb.query.return_value.filter.return_value.first.return_value = None

    response=client.post("/signup",json={ "email": "ui@exampl.com","password": "string@123"})
    print("Response of API is", response.status_code, response.json())
    assert response.status_code==200

def test_invalidEmailformat(mockUser):
    # mockDb.query.return_value.filter.return_value.first.return_value=mockUser
    mockDb.query.return_value.filter.return_value.first.return_value = None

    response=client.post("/signup",json={ "email": "ui@","password": "string@123"})
    print("Response of API is", response.status_code, response.json())
    assert response.status_code==500


def test_invalidPassword(mockUser):
    # mockDb.query.return_value.filter.return_value.first.return_value=mockUser
    mockDb.query.return_value.filter.return_value.first.return_value = None

    response=client.post("/signup",json={ "email": "ui@test.com","password": "S"})
    print("Response of API is", response.status_code, response.json())
    assert response.status_code==500

def test_emptyEmailPass(mockUser):
        mockDb.query.return_value.filter.return_value.first.return_value = None
        response=client.post("/signup", json={"email": "","password": ""})
        print("Response of API is", response.status_code, response.json())
        assert response.status_code!=200
    


def test_userAlreadyRegistered(mockUser):
    mockDb.query.return_value.filter.return_value.first.return_value = mockUser
    # mockDb.query.return_value.filter.return_value.first.return_value = None

    response=client.post("/signup",json={ "email": "test@abc.com","password": "Test91@"})
    print("Response of API is", response.status_code, response.json())
    assert response.status_code==400
    assert response.json()['detail'] == 'Email already registered'


