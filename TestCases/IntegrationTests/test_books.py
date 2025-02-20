
import uuid
import pytest
from httpx import AsyncClient

@pytest.fixture(scope="function")
async def setup_and_teardown():
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        await client.delete('/delete-all-books')

@pytest.fixture
async def get_login_Token():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post('/login', json={"email": "ui@eam.com", "password": "string@123"})
        token = response.json().get("access_token")
        return token

# @pytest.mark.asyncio
# async def test_getHealth():
#     async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
#         response = await client.get('/health')
#         assert response.status_code == 200

@pytest.mark.asyncio
async def test_getBooks(get_login_Token, setup_and_teardown):
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        token = await get_login_Token
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.get('/books', headers=headers, follow_redirects=True)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_AddBook(get_login_Token, setup_and_teardown):
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        token = await get_login_Token
        headers = {'Authorization': f'Bearer {token}'}
        unique_name = str(uuid.uuid4())
        response = await client.post('/books', headers=headers, json={
            "name": unique_name,
            "author": "string",
            "published_year": 0,
            "book_summary": "string"
        }, follow_redirects=True)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_updateBook(get_login_Token, setup_and_teardown):
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        token = await get_login_Token
        headers = {'Authorization': f'Bearer {token}'}
        
        unique_name = str(uuid.uuid4())
        add_response = await client.post('/books', headers=headers, json={
            "name": unique_name,
            "author": "string",
            "published_year": 0,
            "book_summary": "string"
        }, follow_redirects=True)
        book_id = add_response.json().get("id")  
        updated_name = f"Updated {unique_name}"
        update_response = await client.put(f'/books/{book_id}', headers=headers, json={
            "name": updated_name,
            "author": "book",
            "published_year": 0,
            "book_summary": "updated string"
        }, follow_redirects=True)
        
        assert update_response.status_code == 200

@pytest.mark.asyncio
async def test_getBookById(get_login_Token, setup_and_teardown):
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        token = await get_login_Token
        headers = {'Authorization': f'Bearer {token}'}
        
        unique_name = str(uuid.uuid4())
        add_response = await client.post('/books', headers=headers, json={
            "name": unique_name,
            "author": "string",
            "published_year": 0,
            "book_summary": "string"
        }, follow_redirects=True)
        
        book_id = add_response.json().get("id")  
        response = await client.get(f'/books/{book_id}', headers=headers, follow_redirects=True)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_deleteBookById(get_login_Token, setup_and_teardown):
    async with AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        token = await get_login_Token
        headers = {'Authorization': f'Bearer {token}'}
        
        unique_name = str(uuid.uuid4())
        add_response = await client.post('/books', headers=headers, json={
            "name": unique_name,
            "author": "string",
            "published_year": 0,
            "book_summary": "string"
        }, follow_redirects=True)
        
        book_id = add_response.json().get("id")  
        delete_response = await client.delete(f'/books/{book_id}', headers=headers, follow_redirects=True)
        assert delete_response.status_code == 200
