from datetime import datetime
from extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey("hostels.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref="reviews"
    )

    hostel = db.relationship(
        "Hostel",
        back_populates="reviews"
    )

    def __repr__(self):
        return f"<Review {self.id}>"