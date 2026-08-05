from extensions import db

class HostelImage(db.Model):
    __tablename__ = "hostel_images"

    id = db.Column(db.Integer, primary_key=True)

    hostel_id = db.Column(
        db.Integer,
        db.ForeignKey("hostels.id", ondelete="CASCADE"),
        nullable=False
    )

    image = db.Column(
        db.String(255),
        nullable=False
    )

    hostel = db.relationship(
        "Hostel",
        back_populates="images"
    )