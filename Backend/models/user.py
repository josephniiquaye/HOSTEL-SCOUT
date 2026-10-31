from datetime import datetime
from extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    __table_args__ = (
        db.Index("ix_notifications_user_read", "user_id", "is_read"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id}>"

