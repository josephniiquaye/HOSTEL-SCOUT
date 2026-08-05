from datetime import datetime
from extensions import db


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "hostels.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref=db.backref(
            "favorites",
            cascade="all, delete-orphan"
        )
    )

    hostel = db.relationship(
        "Hostel",
        back_populates="favorites"
    )