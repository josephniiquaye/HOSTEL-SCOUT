from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.Index("ix_users_role_created", "role", "created_at"),
        db.Index("ix_users_email_role", "email", "role"),
    )

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(255), nullable=True)

    hostels = db.relationship(
        "Hostel",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.email}>"

