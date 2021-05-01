from flask import Flask
# Imports and sets up the packages SQLAlchemy
# and Migrate(a companion package to SQLAlchemy)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Sets up db and migrate, which are conventional
# variables that give us access to database operations
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    # Configures the app to include two new SQLAlchemy
    # settings:
    # hide a warning about a feature in SQLAlchemy that
    # we won't be using
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connection string for our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # Connects db and migrate to our Flask app,
    # using the package's recommended syntax
    # db and migrate are initialized
    db.init_app(app)
    migrate.init_app(app, db)

    # This code ensures that the Book model will be
    # available to the app when we update our database
    # in a moment.

    # place this import inside a function so that
    # it doesn't run until the function gets called.
    from app.models.book import Book

    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app
