#Model.Py
from flask_login import UserMixin
from . import db

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
    def get_id(self):
        return str(self.id)
    
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    isbn = db.Column(db.String(300), nullable=True)
    file_url = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(300), nullable=True)
    publisher = db.Column(db.String(300), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    department = db.Column(db.Integer, nullable=True)

class BorrowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_title = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    