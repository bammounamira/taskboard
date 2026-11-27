import pytest


def test_create_task_returns_201(client):
    response = client.post("/tasks", json={"title": "Write report"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Write report",
        "description": None,
        "status": "todo",
    }


@pytest.mark.parametrize("payload", [
    {},
    {"title": ""},
    {"title": "   "},
    {"title": None},
    {"title": "x" * 201},
    {"title": "Report", "status": "banana"},
    {"title": "Report", "status": None},
    {"title": "Report", "description": "x" * 2001},
    {"title": "Report", "id": 999},
    {"title": "Report", "owner": "me"},
])
def test_invalid_create_is_rejected(client, payload):
    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    assert client.get("/tasks").json() == []


def test_title_is_trimmed(client):
    response = client.post("/tasks", json={"title": "  Report  "})

    assert response.status_code == 201
    assert response.json()["title"] == "Report"


def test_maximum_lengths_are_accepted(client):
    response = client.post("/tasks", json={
        "title": "t" * 200,
        "description": "d" * 2000,
    })

    assert response.status_code == 201


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_unknown_task_returns_404(client, method):
    kwargs = {"json": {"status": "done"}} if method == "patch" else {}

    response = getattr(client, method)("/tasks/999", **kwargs)

    assert response.status_code == 404


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
@pytest.mark.parametrize("task_id", ["0", "-1", "abc"])
def test_invalid_path_id_is_rejected(client, method, task_id):
    kwargs = {"json": {"status": "done"}} if method == "patch" else {}

    response = getattr(client, method)(f"/tasks/{task_id}", **kwargs)

    assert response.status_code == 422


def test_patch_changes_only_status(client):
    original = client.post("/tasks", json={
        "title": "Report",
        "description": "Keep this",
    }).json()

    response = client.patch(
        f"/tasks/{original['id']}",
        json={"status": "done"},
    )

    assert response.status_code == 200
    assert response.json() == {**original, "status": "done"}


@pytest.mark.parametrize("payload", [
    {"title": None},
    {"status": None},
    {"title": "   "},
    {"title": "x" * 201},
    {"status": "banana"},
    {"description": "x" * 2001},
    {"id": 999},
    {"owner": "me"},
])
def test_invalid_patch_is_rejected(client, payload):
    original = client.post("/tasks", json={"title": "Report"}).json()
    url = f"/tasks/{original['id']}"

    response = client.patch(url, json=payload)

    assert response.status_code == 422
    assert client.get(url).json() == original


def test_patch_can_clear_description(client):
    original = client.post("/tasks", json={
        "title": "Report",
        "description": "Remove this",
    }).json()

    response = client.patch(
        f"/tasks/{original['id']}",
        json={"description": None},
    )

    assert response.status_code == 200
    assert response.json() == {**original, "description": None}


def test_delete_returns_204_then_get_returns_404(client):
    task = client.post("/tasks", json={"title": "Report"}).json()
    url = f"/tasks/{task['id']}"

    response = client.delete(url)

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(url).status_code == 404