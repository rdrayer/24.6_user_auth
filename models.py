"""Models for user auth app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app    
    db.init_app(app)

class User(db.model):
    __tablename__ = 'users'
    def __repr__(self):
        u = self
        return f"{u.id}"
    
    username = db.Column(db.String,
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.String,
                         nullable=False)
    email = db.Column(db.String,
                      unique=True)
    first_name = db.Column(db.String,
                           nullable=False)
    last_name = db.Column(db.String,
                          nullable=False)