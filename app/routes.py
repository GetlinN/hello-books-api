from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify

# Our Blueprint instance. We'll use it to group routes that start with / books.
#  "books" is the debugging name for this Blueprint.
# __name__ provides information the blueprint uses for certain aspects of
# routing.
books_bp = Blueprint("books", __name__, url_prefix="/books")
# A keyword argument. This url_prefix indicates that every endpoint using
# this Blueprint should be treated like it starts with / books. We should
# use this blueprint for all of our RESTful routes that start with /
# books!

# A decorator that uses the books_bp Blueprint to define an endpoint and
# accepted HTTP method. The following function will execute whenever a
# matching HTTP request is received.


@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):

    book = Book.query.get(book_id)
    # book = Book.query.get_or_404(book_id)

    # trying to get one non-existing book and get a 404 response
    if book is None:
        return ({
            "error": True,
            "message": f"Book with id {book_id} is not found."
        }, 404)

    # pull information feature
    if request.method == "GET":
        if book:
            return ({
                "id": book.id,
                "title": book.title,
                "description": book.description
            }, 200)

    # update feature
    elif request.method == "PUT":
        if book:
            form_data = request.get_json()
            book.title = form_data["title"]
            book.description = form_data["description"]
            db.session.commit()
            return make_response(f"Book #{book.id} successfully updated")

    elif request.method == "DELETE":
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response(f"Book #{book.id} successfully deleted")


@books_bp.route("", methods=["GET", "POST"])
def handle_books():

    # # One way we can break this route is to return a response with a status
    # # code 418 before doing anything else in the function.
    # return Response("I'm a teapot!", status=418)

    if request.method == "GET":

        # Finding Books by Title
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            # This SQLAlchemy syntax tells Book to query for all() books. This
            # method returns a list of instances of Book.
            books = Book.query.all()

        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })

        # books_response contains a list of book dictionaries. To turn it into
        # a Response object, we pass it into jsonify(). This will be our common
        # practice when returning a list of something because the make_response
        # function does not handle lists.
        return jsonify(books_response)

    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])

        # db.session is the database's way of collecting changes that need to be
        # made. Here, we are saying we want the database to add new_book.
        db.session.add(new_book)

        # Here, we are saying we want the database to save and commit the
        # collected changes.
        db.session.commit()

        # For each endpoint, we must return the HTTP response
        # make_response: This function instantiates a Response object. A Response
        # object is generally what we want to return from Flask endpoint
        # functions.

        return make_response(
            f"Book {new_book.title} successfully created", 201)

        # return ({
        #     "message": f"Book '{new_book.title}' successfully created"
        # }, 201)

    # hello_world_bp = Blueprint("hello_world", __name__)

    # @hello_world_bp.route("/hello-world", methods=["GET"])
    # def say_hello_world():
    #     my_beautiful_response_body = "Hello, World!"
    #     return my_beautiful_response_body

    # @hello_world_bp.route("/hello-world/JSON", methods=["GET"])
    # def say_hello_json():
    #     return {
    #         "name": "Ada Lovelace",
    #         "message": "Hello!",
    #         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    #     }, 201

    # @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
    # def broken_endpoint():
    #     response_body = {
    #         "name": "Ada Lovelace",
    #         "message": "Hello!",
    #         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    #     }
    #     new_hobby = "Surfing"
    #     response_body["hobbies"] + new_hobby
    #     return response_body
