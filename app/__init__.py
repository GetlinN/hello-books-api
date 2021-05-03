from flask import Flask
# Imports and sets up the packages SQLAlchemy
# and Migrate(a companion package to SQLAlchemy)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# This built - in module provides a way to read environment variables
import os

# Sets up db and migrate, which are conventional
# variables that give us access to database operations
db = SQLAlchemy()
migrate = Migrate()

# loads the values from our .env file so that the os module is able to see
# them.
load_dotenv()


def create_app(test_config=None):
    # parameter test_config should receive a dictionary of configuration
    # settings. It has a default value of None, making the parameter optional.
    app = Flask(__name__)

    if not test_config:
        # None or empty means we are not trying to run the app in a test
        # environment.

        # Configures the app to include two new SQLAlchemy
        # settings:
        # hide a warning about a feature in SQLAlchemy that
        # we won't be using
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # connection string for our database
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
        # os.environ.get() - This syntax gets an environment variable by the
        # passed-in name
    else:
        # we're trying to test the app, which can have special test settings
        app.config["TESTING"] = True  # Turns testing mode on
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")  # testing database environment variabl

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
