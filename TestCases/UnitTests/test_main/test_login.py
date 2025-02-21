from unittest.mock import MagicMock
import bcrypt
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
    print("Entered inside mockUser")
    plain_password = "Test91@"
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return UserCredentials(email='test@abc.com',password=hashed_password)

def test_LoginSuccess(mockUser):
    mockDb.query.return_value.filter.return_value.first.return_value=mockUser

    response=client.post('/login', json={"email":"test@abc.com","password":"Test91@"})
    if response.status_code==200:
            if "access_token" in response.json():
                print("Test Case Passed")
            else:
                assert False, "Test Case Failed since access_token not found"
    else:
        assert False, f'Status Code not 200. Received {response.status_code}'


def test_invalidEmail(mockUser):
    mockDb.query.return_value.filter.return_value.first.return_value=mockUser

    response=client.post("/login", json={"email": "test@g.ca","password": "Test91@"})
    if response.status_code!=200:
        if "access token" not in response.json():
            print("Test Case Passed")

        else:
            assert False, "Test Case Failed"

    else:
        assert False, f'Expected status code like 4XX. Received {response.status_code}' 

def test_invalidPassword(mockUser):
    mockDb.query.return_value.filter.return_value.first.return_value=mockUser

    response=client.post("/login", json={"email": "test@g.ca","password": "Test9"})
    print("response of api is : ", response.status_code)
    assert response.status_code==400 


def test_noEmail(mockUser):
    # print("Mocked User")
    mockDb.query.return_value.filter.return_value.first.return_value = mockUser

    response=client.post("/login", json={"email":"","password":"Test91@"})
    print("Response of API is", response.json())
    assert response.status_code == 400

def test_noPassword(mockUser):
#     print("Mocked User")
    mockDb.query.return_value.filter.return_value.first.return_value = mockUser

    response=client.post("/login", json={"email":"test@abc.com","password":""})
    print("Response of API is", response.json(), response.status_code)
    assert response.status_code == 400

def test_NoEMailandPassword(mockUser):
   
    mockDb.query.return_value.filter.return_value.first.return_value = mockUser

    response=client.post("/login",json={"email":"","password":""})
    print("response of api", response.status_code)
    assert response.status_code==400
