from fastapi.testclient import TestClient

from main import app,get_db
from database import sessionLocal
import models


client = TestClient(app)

def override_get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db 

def get_access_token():
    response = client.post('/auth/token',data={
        'username':'okok',
        'password':'1234'
    })
    token = response.json()['access_token']
    return {
        "Authorization": f"Bearer {token}"
    }

def test_add_book():
    response = client.post('/books',json={'title':'things you cant lie','author':'idk','price':100},headers=get_access_token())

    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'things you cant lie'
    assert data['author'] == 'idk'
    assert 'id' in data
    assert data['price'] == 100



def test_get_all_books():
    response = client.get("/books")

    assert response.status_code == 200

    data = response.json()
    print(data)

    assert data[0]["title"] == "things you cant lie"
    assert data[0]["author"] == "idk"

def test_perticular_book():
    response = client.get('/books/1')

    assert response.status_code == 200
    data = response.json()

    assert data['title'] =="things you cant lie"
    assert data["author"] == "idk" 

def test_update_book():
    response = client.put(
        "/books/1",
        json={
            "title": "updated title",
            "author": "new author",
            "price": 500
        },
        headers=get_access_token()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "updated title"
    assert data["author"] == "new author"
    assert data["price"] == 500
    assert data["id"] == 1

def test_delete_book():
    response = client.delete(
        "/books/1",
        headers=get_access_token()
    )

    assert response.status_code == 200