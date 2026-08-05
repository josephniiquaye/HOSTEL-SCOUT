from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from extensions import db
from models.review import Review
from models.booking import Booking
from models.hostel import Hostel

review = Blueprint("review", __name__)


@review.route("/review/<int:hostel_id>", methods=["GET", "POST"])
def add_review(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    hostel = Hostel.query.get_or_404(hostel_id)

    # Student must have an approved booking
    approved_booking = Booking.query.filter_by(
        student_id=session["user_id"],
        hostel_id=hostel.id,
        status="Approved"
    ).first()

    if not approved_booking:
        flash(
            "You can only review a hostel after an approved booking.",
            "warning"
        )
        return redirect(
            url_for("hostel.hostel_details", hostel_id=hostel.id)
        )

    # Prevent duplicate reviews
    existing_review = Review.query.filter_by(
        student_id=session["user_id"],
        hostel_id=hostel.id
    ).first()

    if existing_review:
        flash("You have already reviewed this hostel.", "info")
        return redirect(
            url_for("hostel.hostel_details", hostel_id=hostel.id)
        )

    if request.method == "POST":

        review = Review(
            student_id=session["user_id"],
            hostel_id=hostel.id,
            rating=int(request.form["rating"]),
            comment=request.form["comment"]
        )

        db.session.add(review)
        db.session.commit()

        flash("Thank you for your review!", "success")

        return redirect(
            url_for("hostel.hostel_details", hostel_id=hostel.id)
        )

    return render_template(
        "add_review.html",
        hostel=hostel
    )