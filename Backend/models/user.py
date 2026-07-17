from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="student")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"