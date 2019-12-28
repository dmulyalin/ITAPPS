from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
import base64
from datetime import datetime, timedelta
import os

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    api_token = db.Column(db.String(32), index=True, unique=True)
    api_token_expiration = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)  
    
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)
    
    # API token authentication methods
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.api_token and self.api_token_expiration > now + timedelta(seconds=60):
            return self.api_token
        self.api_token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.api_token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        print("adding token for client")
        return self.api_token

    def revoke_token(self):
        self.api_token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(api_token):
        user = User.query.filter_by(api_token=api_token).first()
        if user is None or user.api_token_expiration < datetime.utcnow():
            return None
        return user