# access to the SQLAlchemy db
from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    # specify a different name for the table,
    __tablename__ = "books"
