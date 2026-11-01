from io import BytesIO

from flask import (
    Blueprint,
    send_file,
    session,
    redirect,
    url_for,
    flash
)

from reportlab.pdfgen import canvas

from models.booking import Booking
from models.user import User
from models.hostel import Hostel
from models.review import Review

pdf = Blueprint("pdf", __name__)


# ======================================================
# STUDENT BOOKING RECEIPT
# ======================================================

@pdf.route("/receipt/<int:booking_id>")
def booking_receipt(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.student_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("booking.my_bookings"))

    if booking.status != "Approved":
        flash(
            "Receipt is available only for approved bookings.",
            "warning"
        )
        return redirect(url_for("booking.my_bookings"))

    buffer = BytesIO()

    pdf_file = canvas.Canvas(buffer)

    pdf_file.setFont("Helvetica-Bold", 20)
    pdf_file.drawString(170, 800, "HOSTEL SCOUT")

    pdf_file.setFont("Helvetica", 12)

    y = 760

    pdf_file.drawString(
        50,
        y,
        f"Receipt No: HS-{booking.id:05d}"
    )

    y -= 30

    pdf_file.drawString(
        50,
        y,
        f"Student: {booking.student.fullname}"
    )

    y -= 25

    pdf_file.drawString(
        50,
        y,
        f"Hostel: {booking.hostel.name}"
    )

    y -= 25

    pdf_file.drawString(
        50,
        y,
        f"Location: {booking.hostel.location}"
    )

    y -= 25

    pdf_file.drawString(
        50,
        y,
        f"Price: GH₵ {booking.occupancy.price if booking.occupancy else booking.hostel.price}"
    )

    y -= 25

    pdf_file.drawString(
        50,
        y,
        f"Status: {booking.status}"
    )

    y -= 25

    pdf_file.drawString(
        50,
        y,
        f"Booking Date: {booking.created_at.strftime('%d %B %Y')}"
    )

    y -= 50

    pdf_file.line(50, y, 550, y)

    y -= 30

    pdf_file.drawString(
        50,
        y,
        "Thank you for choosing HOSTEL SCOUT."
    )

    pdf_file.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Receipt_{booking.id}.pdf",
        mimetype="application/pdf"
    )


# ======================================================
# ADMIN SYSTEM REPORT
# ======================================================

@pdf.route("/generate-report")
def generate_report():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash("Unauthorized.", "danger")
        return redirect(url_for("home"))

    total_users = User.query.count()

    students = User.query.filter_by(
        role="student"
    ).count()

    owners = User.query.filter_by(
        role="owner"
    ).count()

    admins = User.query.filter_by(
        role="admin"
    ).count()

    total_hostels = Hostel.query.count()

    total_bookings = Booking.query.count()

    pending = Booking.query.filter_by(
        status="Pending"
    ).count()

    approved = Booking.query.filter_by(
        status="Approved"
    ).count()

    rejected = Booking.query.filter_by(
        status="Rejected"
    ).count()

    total_reviews = Review.query.count()

    buffer = BytesIO()

    pdf_file = canvas.Canvas(buffer)

    pdf_file.setTitle("HOSTEL SCOUT System Report")

    pdf_file.setFont("Helvetica-Bold", 22)

    pdf_file.drawString(
        150,
        800,
        "HOSTEL SCOUT"
    )

    pdf_file.setFont("Helvetica-Bold", 16)

    pdf_file.drawString(
        170,
        775,
        "SYSTEM REPORT"
    )

    pdf_file.setFont("Helvetica", 12)

    y = 730

    pdf_file.drawString(50, y, f"Total Users: {total_users}")
    y -= 22

    pdf_file.drawString(50, y, f"Students: {students}")
    y -= 22

    pdf_file.drawString(50, y, f"Hostel Owners: {owners}")
    y -= 22

    pdf_file.drawString(50, y, f"Administrators: {admins}")
    y -= 22

    pdf_file.drawString(50, y, f"Hostels: {total_hostels}")
    y -= 22

    pdf_file.drawString(50, y, f"Bookings: {total_bookings}")
    y -= 22

    pdf_file.drawString(50, y, f"Pending Bookings: {pending}")
    y -= 22

    pdf_file.drawString(50, y, f"Approved Bookings: {approved}")
    y -= 22

    pdf_file.drawString(50, y, f"Rejected Bookings: {rejected}")
    y -= 22

    pdf_file.drawString(50, y, f"Reviews: {total_reviews}")

    y -= 50

    pdf_file.line(50, y, 550, y)

    y -= 30

    pdf_file.drawString(
        50,
        y,
        "Generated automatically by HOSTEL SCOUT."
    )

    pdf_file.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="HOSTEL_SCOUT_System_Report.pdf",
        mimetype="application/pdf"
    )