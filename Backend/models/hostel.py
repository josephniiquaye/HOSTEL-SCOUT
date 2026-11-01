from datetime import datetime
from extensions import db


class Hostel(db.Model):
    __tablename__ = "hostels"

    id = db.Column(db.Integer, primary_key=True)

    facilities = db.Column(db.Text, nullable=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(150),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    # Default price shown in hostel listings
    single_price = db.Column(
        db.Float,
        nullable=True
    )

    double_price = db.Column(
        db.Float,
        nullable=True
    )

    triple_price = db.Column(
        db.Float,
        nullable=True
    )

    quad_price = db.Column(
        db.Float,
        nullable=True
    )

    # Number of spaces available for each occupancy
    single_rooms = db.Column(
        db.Integer,
        default=0
    )

    double_rooms = db.Column(
        db.Integer,
        default=0
    )

    triple_rooms = db.Column(
        db.Integer,
        default=0
    )

    quad_rooms = db.Column(
        db.Integer,
        default=0
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )
    
    map_link = db.Column(
        db.String(500),
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    owner = db.relationship(
        "User",
        back_populates="hostels"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="hostel",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="hostel",
        cascade="all, delete-orphan"
    )

    images = db.relationship(
        "HostelImage",
        back_populates="hostel",
        cascade="all, delete-orphan",
        lazy="select"
    )

    favorites = db.relationship(
        "Favorite",
        back_populates="hostel",
        cascade="all, delete-orphan"
    )
    
    occupancies = db.relationship(
        "Occupancy",
        back_populates="hostel",
        cascade="all, delete-orphan"
    )

    @property
    def average_rating(self):
        if not self.reviews:
            return 0

        total = sum(review.rating for review in self.reviews)

        return round(total / len(self.reviews), 1)
    
    @property
    def is_full(self):
        return all(
            room.rooms_available <= 0
            for room in self.occupancies
        )

    # TODO: The rooms_available DB column has been replaced by this property.
    # Run a migration to drop the rooms_available column from the hostels table when ready.
    @property
    def rooms_available(self):
        return sum(o.rooms_available for o in self.occupancies)

    @property
    def review_count(self):
        return len(self.reviews)
    
    @property
    def facility_list(self):
        if not self.facilities:
            return []

        return self.facilities.split(",")

    def __repr__(self):
        return (
            f"<Hostel "
            f"id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status}'>"
        )