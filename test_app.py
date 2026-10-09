from fastapi.testclient import TestClient

from exam_project.main import app

client = TestClient(app)


def test_create_and_list_categories():
    response = client.post("/categories/", json={"name": "Fiction"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Fiction"

    response = client.get("/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert any(item["name"] == "Fiction" for item in categories)


def test_create_book_and_fetch_by_id():
    category = client.post("/categories/", json={"name": "Science"}).json()

    response = client.post(
        "/books/",
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
            "isbn": "9780735211292",
            "stock_quantity": 10,
            "category_id": category["id"],
        },
    )
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == "Atomic Habits"
    assert book["category_id"] == category["id"]

    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Atomic Habits"


def test_update_delete_and_error_handling():
    category = client.post("/categories/", json={"name": "History"}).json()
    response = client.post(
        "/books/",
        json={
            "title": "The Rise of the Roman Empire",
            "author": "A. Smith",
            "isbn": "9780000000001",
            "stock_quantity": 5,
            "category_id": category["id"],
        },
    )
    book = response.json()

    response = client.put(
        f"/books/{book['id']}",
        json={"title": "Updated Roman Empire", "stock_quantity": 8},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Roman Empire"
    assert response.json()["stock_quantity"] == 8

    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    response = client.get("/books/9999")
    assert response.status_code == 404

    response = client.post(
        "/books/",
        json={
            "title": "Bad Book",
            "author": "No One",
            "isbn": "9780000000001",
            "stock_quantity": 2,
            "category_id": 9999,
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/books/",
        json={
            "title": "Duplicate ISBN",
            "author": "Author",
            "isbn": "9780735211292",
            "stock_quantity": 1,
            "category_id": category["id"],
        },
    )
    assert response.status_code == 400
