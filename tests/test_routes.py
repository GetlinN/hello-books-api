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
    """
    1. GET /books/1 returns a response body that
    matches our fixture
    """
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


def test_get_no_data(client):
    """
    2. GET /books/1 with no data in test database
    (no fixture) returns a 404
    """
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'error': True,
                             'message': 'Book with id 1 is not found.'}


def test_get_all_books(client, two_saved_books):
    """
    3. GET /books with valid test data (fixtures)
    returns a 200 with an array including
    appropriate test data
    """
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2


def test_post_book(client):
    """
    POST /books with a JSON request body returns a 201
    """
    request_body = {
        "title": "Lake Book",
        "description": "lake take make"
    }

    # Act
    response = client.post("/books", json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": f"Book '{request_body['title']}' successfully created"
    }
