from extensions import db


class Occupancy(db.Model):
    __tablename__ = "occupancies"

    id = db.Column(db.Integer, primary_key=True)

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey("hostels.id"),
        nullable=False
    )

    occupancy = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    rooms_available = db.Column(
        db.Integer,
        default=0
    )

    hostel = db.relationship(
        "Hostel",
        back_populates="occupancies"
    )
    
    bookings = db.relationship(
       'Booking',
       back_populates="occupancy"
    )