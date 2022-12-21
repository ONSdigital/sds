from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)


def test_publish():
    with open("data/data_set.json") as f:
        dataset = json.load(f)
    response = client.put("/publish", json=dataset)
    print(response.text)
    assert response.status_code == 200