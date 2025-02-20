import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlalchemy.orm import Session
from bookstore.main import app, get_db
from bookstore.database import Book, UserCredentials
from bookstore.middleware import JWTBearer
from passlib.context import CryptContext


client = TestClient(app)
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def mock_db():
    mock_db_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_user = UserCredentials(email="test@abcd.com", password=pwd.hash("testing@912"))
    mock_books = [
        Book(id=1, name="Test1", author="Testing Author 1",published_year=2015, book_summary="TESTING QA DESC"),
        Book(id=2, name="Test2", author="Testing Author 2",published_year=2015, book_summary="TESTING QA2 DESC"),
    ]
    mock_query.all.return_value = mock_books
    mock_query.filter.return_value.first.return_value = lambda:mock_books[1]
    mock_db_session.query.return_value = mock_query  
    return mock_db_session


@pytest.fixture
def mockUser():
    print("Entered inside mockUser")
    return UserCredentials(email='test@abc.com', password=pwd.hash("Test91@"))


@pytest.fixture
def override_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

@pytest.fixture
def getAuthToken(mock_db, mockUser, override_db):
    mock_db.query.return_value.filter.return_value.first.return_value = mockUser 
    response = client.post('/login', json={"email": "test@abc.com", "password": "Test91@"})
    print("Response from API is", response.json())
    token = response.json().get("access_token")

    
    return token

def test_getBook(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.get("/books", headers=headers)
    
    print("Response from API:", response.status_code, response.json())
    
    assert response.status_code == 200




def test_addBook(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.post("/books", headers=headers, json={"name": "New",
                                                            "author": "TestQA",
                                                            "published_year": 2015,
                                                            "book_summary": "Description test"})
    
    print("Response from API:", response.status_code, response.json())
    
    assert response.status_code == 200

def test_addBookWithInvalidJson(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.post('/books',headers=headers, json={"text": "Testing book"})
    assert response.status_code == 422


def test_addBookWithoutToken(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.post("/books", json={"name": "New",
                                                            "author": "TestQA",
                                                            "published_year": 2015,
                                                            "book_summary": "Description test"})
    
    print("Response from API:", response.status_code, response.json())
    
    assert response.status_code != 200


def test_deleteBook(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.delete("/books/1", headers=headers)
    
    print("Response from API:", response.status_code, response.json())
    assert response.status_code == 200

def test_deleteUnknownBook(getAuthToken):
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.delete("/books/8", headers=headers)
    print("Response from API:", response.status_code, response.json())
    assert response.status_code == 404


def test_get_book_by_id_success(getAuthToken, mock_db):
    book_id = 1  
    book_data = {
        "id": book_id,
        "name": "Test Book",
        "author": "Author Name",
        "published_year": 2021,
        "book_summary": "Test Book Summary"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = book_data
    
    headers = {"Authorization": f"Bearer {getAuthToken}"}
    response = client.get(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == book_data
