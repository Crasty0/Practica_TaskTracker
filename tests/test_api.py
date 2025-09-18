from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_flow(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test_tasks.db")
    monkeypatch.setenv("TASKS_DB", db_file)


# Re-import parts to ensure DB path changed (simple approach)
from importlib import reload
import app.db as dbmod
reload(dbmod)
from app.db import Base, engine
Base.metadata.create_all(bind=engine)


headers = {"X-User": "tester"}


# create
r = client.post("/tasks", json={"title": "Task1", "description": "desc"}, headers=headers)
assert r.status_code == 200
data = r.json()
assert data["title"] == "Task1"
task_id = data["id"]


# list
r = client.get("/tasks", headers=headers)
assert r.status_code == 200
lst = r.json()
assert any(t["id"] == task_id for t in lst)


# update
r = client.put(f"/tasks/{task_id}", json={"status": "in-progress"}, headers=headers)
assert r.status_code == 200
assert r.json()["status"] == "in-progress"


# delete
r = client.delete(f"/tasks/{task_id}", headers=headers)
assert r.status_code == 200
assert r.json()["ok"] is True


# not found after delete
r = client.get(f"/tasks/{task_id}", headers=headers)
assert r.status_code == 404