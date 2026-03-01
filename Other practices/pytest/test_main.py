from main import app ,get_db
from database import sessionLocal
from fastapi.testclient import TestClient

def override_get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_auth_token():
    response = client.post('/auth/token',data={
        'username':'okok',
        'password':'1234'
    })

    assert response.status_code == 200
    return response.json()["access_token"]

def test_all_user():
    response = client.get('/users',headers={'Authorization':f'Bearer {get_auth_token()}'})
    assert response.status_code == 200

def test_add_game():
    response = client.post('/games',json={'id':1,'name':'valorant','size':10},headers={
        'Authorization':f'Bearer {get_auth_token()}'
    })

    assert response.status_code == 201
    assert response.json() == {'id':1,'name':'valorant','size':10}
