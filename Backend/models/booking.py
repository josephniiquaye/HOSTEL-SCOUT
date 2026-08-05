from datetime import datetime
from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

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

    # NEW
    occupancy_id = db.Column(
        db.Integer,
        db.ForeignKey("occupancies.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref="bookings"
    )

    hostel = db.relationship(
        "Hostel",
        back_populates="bookings"
    )

    occupancy = db.relationship(
        "Occupancy",
        back_populates="bookings"
    )

    def __repr__(self):
        return f"<Booking {self.id}>"