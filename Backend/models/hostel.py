from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash
)


from sqlalchemy import func, or_  # type: ignore
from dotenv import load_dotenv
load_dotenv()
from config import Config
from extensions import db, migrate, mail


from models.hostel import Hostel
from models.booking import Booking
from models.user import User
from models.notification import Notification
from models.review import Review
from models.announcement import Announcement
from models.hostel_image import HostelImage
from models.occupancy import Occupancy

from routes.auth import auth
from routes.hostel import hostel
from routes.booking import booking
from routes.review import review
from routes.favorite import favorite
from routes.notification import notification
from routes.pdf import pdf

from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime


app = Flask(__name__)

app.config.from_object(Config)

print("Loaded MAIL_SERVER:", app.config.get("MAIL_SERVER"))
print("Loaded MAIL_PORT:", app.config.get("MAIL_PORT"))
print("Loaded Config:", Config)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)


app.register_blueprint(auth)
app.register_blueprint(hostel)
app.register_blueprint(booking)
app.register_blueprint(review)
app.register_blueprint(favorite)
app.register_blueprint(notification)
app.register_blueprint(pdf)


@app.route("/")
def home():
    """Render the homepage with optional filtering and sorting for hostels."""

    search = request.args.get("search")
    location = request.args.get("location")
    gender = request.args.get("gender")
    max_price = request.args.get("price")
    rating = request.args.get("rating")
    available = request.args.get("available")
    sort = request.args.get("sort")
    page = request.args.get("page", 1, type=int)
    per_page = min(max(request.args.get("per_page", 12, type=int), 6), 24)

    query = Hostel.query.filter_by(status="Approved")

    if search:
        query = query.filter(
            or_(
                Hostel.name.ilike(f"%{search}%"),
                Hostel.location.ilike(f"%{search}%")
            )
        )

    if location:
        query = query.filter(Hostel.location.ilike(f"%{location}%"))

    if gender:
        query = query.filter(Hostel.gender == gender)

    if max_price:
        query = query.filter(Hostel.price <= float(max_price))

    if available:
        query = query.filter(Hostel.rooms_available > 0)

    if sort == "low":
        query = query.order_by(Hostel.price.asc())
    elif sort == "high":
        query = query.order_by(Hostel.price.desc())
    else:
        query = query.order_by(Hostel.created_at.desc())

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    hostels = paginated.items

    if rating:
        hostels = [h for h in hostels if h.average_rating >= float(rating)]

    if sort == "low":
        hostels = sorted(hostels, key=lambda h: h.price)
    elif sort == "high":
        hostels = sorted(hostels, key=lambda h: h.price, reverse=True)
    elif sort == "rating":
        hostels = sorted(hostels, key=lambda h: h.average_rating, reverse=True)
    else:
        hostels = sorted(hostels, key=lambda h: h.created_at, reverse=True)

    featured_hostels = Hostel.query.filter_by(status="Approved").order_by(
        Hostel.created_at.desc()
    ).limit(4).all()

    return render_template(
        "index.html",
        hostels=hostels,
        featured_hostels=featured_hostels,
        pagination=paginated,
    )


@app.route("/student-dashboard")
def student_dashboard():
    """Student dashboard route displaying all hostels."""
    hostels = Hostel.query.order_by(Hostel.created_at.desc()).limit(50).all()
    return render_template("student_dashboard.html", hostels=hostels)


@app.route("/owner-dashboard")
def owner_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "owner":
        return redirect(url_for("student_dashboard"))

    hostel_count = Hostel.query.filter_by(owner_id=session["user_id"]).count()

    total_rooms = db.session.query(func.sum(Hostel.rooms_available)).filter(
        Hostel.owner_id == session["user_id"]
    ).scalar()

    if total_rooms is None:
        total_rooms = 0

    booking_count = Booking.query.join(Hostel).filter(
        Hostel.owner_id == session["user_id"]
    ).count()

    pending_bookings = Booking.query.join(Hostel).filter(
        Hostel.owner_id == session["user_id"],
        Booking.status == "Pending"
    ).count()

    return render_template(
        "owner_dashboard.html",
        hostel_count=hostel_count,
        total_rooms=total_rooms,
        booking_count=booking_count,
        pending_bookings=pending_bookings
    )


@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return redirect(url_for("home"))

    total_users = User.query.count()
    students = User.query.filter_by(role="student").count()
    owners = User.query.filter_by(role="owner").count()
    admins = User.query.filter_by(role="admin").count()
    total_hostels = Hostel.query.count()
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status="Pending").count()
    approved_bookings = Booking.query.filter_by(status="Approved").count()
    rejected_bookings = Booking.query.filter_by(status="Rejected").count()
    total_reviews = Review.query.count()
    users = User.query.order_by(User.id.desc()).limit(50).all()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(20).all()
    pending_hostels = Hostel.query.filter_by(status="Pending").limit(50).all()
    approved_hostels = Hostel.query.filter_by(status="Approved").count()
    rejected_hostels = Hostel.query.filter_by(status="Rejected").count()

    top_hostels = sorted(
        Hostel.query.filter_by(status="Approved").all(),
        key=lambda h: h.average_rating,
        reverse=True
    )[:5]

    hostel_names = [h.name for h in top_hostels]
    hostel_ratings = [h.average_rating for h in top_hostels]

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        students=students,
        owners=owners,
        admins=admins,
        total_hostels=total_hostels,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        approved_bookings=approved_bookings,
        rejected_bookings=rejected_bookings,
        total_reviews=total_reviews,
        users=users,
        pending_hostels=pending_hostels,
        approved_hostels=approved_hostels,
        rejected_hostels=rejected_hostels,
        hostel_names=hostel_names,
        hostel_ratings=hostel_ratings,
        announcements=announcements,
    )


@app.route("/admin/announcement/add", methods=["POST"])
def add_announcement():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return redirect(url_for("home"))

    title = request.form.get("title")
    message = request.form.get("message")

    announcement = Announcement(title=title, message=message)
    db.session.add(announcement)

    users = User.query.all()
    notifications = [
        Notification(
            user_id=user.id,
            message=f"📢 {title}\n\n{message}",
            is_read=False,
        )
        for user in users
    ]
    db.session.add_all(notifications)
    db.session.commit()

    flash("Announcement published successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/announcement/delete/<int:id>")
def delete_announcement(id):
    """Delete an announcement by id for admin users."""

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return redirect(url_for("home"))

    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()

    flash("Announcement deleted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-user/<int:user_id>")
def delete_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)

    if user.id == session["user_id"]:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin_dashboard"))

    if user.role == "admin":
        flash("Admin accounts cannot be deleted.", "danger")
        return redirect(url_for("admin_dashboard"))

    if user.role == "student":
        Booking.query.filter_by(student_id=user.id).delete()
    elif user.role == "owner":
        hostels = Hostel.query.filter_by(owner_id=user.id).all()
        for h in hostels:
            Booking.query.filter_by(hostel_id=h.id).delete()
            db.session.delete(h)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.context_processor
def notification_count():

    if "user_id" not in session:
        return dict(unread_notifications=0)

    unread = Notification.query.filter_by(
        user_id=session["user_id"],
        is_read=False
    ).count()

    return dict(unread_notifications=unread)


@app.route("/test-email")
def test_email():
    print("MAIL_SERVER:", app.config["MAIL_SERVER"])
    print("MAIL_PORT:", app.config["MAIL_PORT"])
    print("MAIL_USE_TLS:", app.config["MAIL_USE_TLS"])
    print("MAIL_USE_SSL:", app.config.get("MAIL_USE_SSL"))

    msg = Message(
        subject="HOSTEL SCOUT Test",
        recipients=["josephniiquaye84@gmail.com"]
    )

    msg.body = "Testing email."
    mail.send(msg)

    return "Sent!"


@app.route("/verify/<token>")
def verify_email(token):

    try:
        email = serializer.loads(
            token,
            salt="email-confirm",
            max_age=3600
        )

    except Exception:
        flash("Verification link has expired.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    user.is_verified = True
    db.session.commit()

    flash("Email verified successfully.", "success")
    return redirect(url_for("auth.login"))


@app.context_processor
def inject_current_user():

    user = None

    if "user_id" in session:
        user = User.query.get(session["user_id"])

    return dict(current_user=user)


if __name__ == "__main__":
    app.run(debug=True)

