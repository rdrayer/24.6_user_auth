"""Models for user auth app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app    
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    def __repr__(self):
        u = self
        return f"{u.username} {u.password} {u.email} {u.first_name} {u.last_name}"
    
    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.String,
                         nullable=False)
    email = db.Column(db.String(50),
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register new user w/hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,
                    password=hashed_utf8,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        '''Validate user exists and pw matches'''
        '''Return User if valid, else return false'''
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False