from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from flask_mail import Message

from extensions import db, mail

from models.booking import Booking
from models.hostel import Hostel
from models.notification import Notification
from models.user import User
from models.occupancy import Occupancy


booking = Blueprint("booking", __name__)


@booking.route("/book/<int:hostel_id>/<int:occupancy_id>")
def book_hostel(hostel_id, occupancy_id):

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    if session.get("role") != "student":
        flash("Only students can book hostels.", "danger")
        return redirect(url_for("home"))

    hostel = Hostel.query.get_or_404(hostel_id)

    occupancy = Occupancy.query.get_or_404(occupancy_id)

    # Ensure the occupancy belongs to this hostel
    if occupancy.hostel_id != hostel.id:
        flash("Invalid occupancy selected.", "danger")
        return redirect(
            url_for(
                "hostel.hostel_details",
                hostel_id=hostel.id
            )
        )

    # Check availability
    if occupancy.rooms_available <= 0:
        flash(
            f"{occupancy.occupancy} is currently full.",
            "warning"
        )
        return redirect(
            url_for(
                "hostel.hostel_details",
                hostel_id=hostel.id
            )
        )

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by(
        student_id=session["user_id"],
        occupancy_id=occupancy.id
    ).first()

    if existing_booking:
        flash(
            "You have already booked this occupancy.",
            "info"
        )
        return redirect(
            url_for(
                "hostel.hostel_details",
                hostel_id=hostel.id
            )
        )

    # Create booking
    new_booking = Booking(
        student_id=session["user_id"],
        hostel_id=hostel.id,
        occupancy_id=occupancy.id
    )

    db.session.add(new_booking)

    

    student = User.query.get(session["user_id"])

    notification = Notification(
        user_id=hostel.owner_id,
        message=(
            f"You have received a new booking request "
            f"for '{hostel.name}' "
            f"({occupancy.occupancy}) "
            f"from {student.fullname}."
        )
    )

    db.session.add(notification)

    owner = hostel.owner

    if owner:

        msg = Message(
            subject="HOSTEL SCOUT - New Booking Request",
            recipients=[owner.email]
        )

        msg.body = f"""
Hello {owner.fullname},

You have received a new booking request.

Student:
{student.fullname}

Hostel:
{hostel.name}

Occupancy:
{occupancy.occupancy}

Price:
GH₵ {occupancy.price}

Please log into HOSTEL SCOUT to approve or reject the booking.

Thank you.

HOSTEL SCOUT
"""

        try:
            mail.send(msg)

        except Exception as e:
            print("EMAIL ERROR:", e)

    db.session.commit()

    flash(
        "Booking submitted successfully!",
        "success"
    )

    return redirect(
        url_for("booking.my_bookings")
    )


@booking.route("/my-bookings")
def my_bookings():
    """Display bookings for the currently logged-in student.

    Redirects to login if no user is in session.
    """

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    bookings = Booking.query.filter_by(
        student_id=session["user_id"]
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


@booking.route("/owner/bookings")
def owner_bookings():
    """Display bookings for the currently logged-in owner.

    Redirects to login if no user is in session and to the student
    dashboard if the current user is not an owner.
    """

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "owner":
        return redirect(url_for("student_dashboard"))

    bookings = Booking.query.join(Hostel).filter(
        Hostel.owner_id == session["user_id"]
    ).all()

    return render_template(
        "owner_bookings.html",
        bookings=bookings
    )


# ===================================================
# APPROVE BOOKING
# ===================================================

@booking.route("/approve-booking/<int:booking_id>", methods=["POST"])
def approve_booking(booking_id):
    """Approve a booking: verify owner, update status, notify student and send email."""

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('booking.owner_bookings'))

    booking_record = Booking.query.get_or_404(booking_id)
    
    if booking_record.hostel.owner_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("booking.owner_bookings"))
    
    if booking_record.status != "Pending":
        flash(
            "This booking has already been processed.",
            "warning"
        )
        return redirect(
            url_for("booking.owner_bookings")
        )

    booking_record.status = "Approved"
    
    # Reduce occupancy after approval only

    booking_record.occupancy.rooms_available -= 1
    if booking_record.occupancy.rooms_available < 0:
        booking_record.occupancy.rooms_available = 0

    student = User.query.get(booking_record.student_id)
    hostel = booking_record.hostel

    notification = Notification(
        user_id=student.id,
        message=f"🎉 Your booking for '{hostel.name}' has been approved."
    )

    db.session.add(notification)

    if student:

        msg = Message(
            subject="HOSTEL SCOUT - Booking Approved",
            recipients=[student.email]
        )

        msg.body = f"""
Hello {student.fullname},

Congratulations!

Your booking request for

{hostel.name}

has been APPROVED.

You can now contact the hostel owner and complete your move-in process.

Thank you for using HOSTEL SCOUT.
"""

        try:
            mail.send(msg)
        except Exception as e:
            print("EMAIL ERROR:", e)

    db.session.commit()

    flash("Booking approved successfully.", "success")

    return redirect(url_for("booking.owner_bookings"))


# ===================================================
# REJECT BOOKING
# ===================================================

@booking.route("/reject-booking/<int:booking_id>", methods=["POST"])
def reject_booking(booking_id):
    """Reject a booking as the hostel owner."""

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('booking.owner_bookings'))

    booking = Booking.query.get_or_404(booking_id)

    if booking.hostel.owner_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("booking.owner_bookings"))

    # FIRST: check if already processed
    if booking.status != "Pending":
        flash(
            "This booking has already been processed.",
            "warning"
        )
        return redirect(url_for("booking.owner_bookings"))

    # THEN: set status
    booking.status = "Rejected"

    student = User.query.get(booking.student_id)
    hostel = booking.hostel

    notification = Notification(
        user_id=student.id,
        message=f"❌ Your booking for '{hostel.name}' has been rejected."
    )

    db.session.add(notification)

    if student:

        msg = Message(
            subject="HOSTEL SCOUT - Booking Rejected",
            recipients=[student.email]
        )

        msg.body = f"""
Hello {student.fullname},

Unfortunately,

your booking request for

{hostel.name}

has been REJECTED.

You may browse other available hostels on HOSTEL SCOUT.

Thank you.
"""

        try:
            mail.send(msg)
        except Exception as e:
            print("EMAIL ERROR:", e)

    db.session.commit()

    flash("Booking rejected.", "warning")

    return redirect(url_for("booking.owner_bookings"))

@booking.route("/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):
    """Handle cancellation of a pending booking by the student."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    booking = Booking.query.get_or_404(booking_id)

    # Only the student who made the booking can cancel it
    if booking.student_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("booking.my_bookings"))

    # Prevent cancelling completed decisions
    if booking.status != "Pending":
        flash(
            "Only pending bookings can be cancelled.",
            "warning"
        )
        return redirect(url_for("booking.my_bookings"))

    booking.status = "Cancelled"

    owner = booking.hostel.owner
    student = booking.student
    hostel = booking.hostel

    # ---------------------------------------
    # Owner Notification
    # ---------------------------------------

    notification = Notification(
        user_id=owner.id,
        message=f" {student.fullname} cancelled their booking for '{hostel.name}'."
    )

    db.session.add(notification)

    # ---------------------------------------
    # Email Owner
    # ---------------------------------------

    msg = Message(
        subject="HOSTEL SCOUT - Booking Cancelled",
        recipients=[owner.email]
    )

    msg.body = f"""
Hello {owner.fullname},

The following booking has been cancelled.

Student:
{student.fullname}

Hostel:
{hostel.name}

No further action is required.

HOSTEL SCOUT
"""

    try:
        mail.send(msg)

    except Exception as e:
        print("EMAIL ERROR:", e)

    db.session.commit()

    flash(
        "Booking cancelled successfully.",
        "success"
    )

    return redirect(url_for("booking.my_bookings"))