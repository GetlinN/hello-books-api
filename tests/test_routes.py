# This file will hold the tests for the code in our app / routes.py file.

def test_get_all_books_with_no_records(client):
    # Act
    # This sends an HTTP request to / books. It returns an HTTP response object, which we store in our local variable response
    # We pass in the client fixture here, which we registered in conftest.py.
    # pytest automatically tries to match each test parameter to a fixture
    # with the same name.
    response = client.get("/books")
    # We can get the JSON response body with response.get_json()
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
