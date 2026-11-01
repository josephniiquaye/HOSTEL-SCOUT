import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
)

from flask import current_app
from werkzeug.utils import secure_filename

from extensions import db
from models.hostel import Hostel
from models.user import User
from models.favorite import Favorite
from models.review import Review
from models.booking import Booking
from flask_mail import Message
from extensions import mail
from models.notification import Notification
from models.hostel_image import HostelImage
from models.occupancy import Occupancy


hostel = Blueprint("hostel", __name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def allowed_file(filename):
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS

@hostel.route("/add-hostel", methods=["GET", "POST"])
def add_hostel():
    """Add a new hostel listing."""

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if user.role != "owner":
        flash("Only hostel owners can add hostels.", "danger")
        return redirect(url_for("student_dashboard"))

    if request.method == "POST":

        upload_path = os.path.join(
            current_app.static_folder,
            "uploads"
        )

        os.makedirs(upload_path, exist_ok=True)

        # -------------------------------
        # Hostel Facilities
        # -------------------------------

        facilities = request.form.getlist("facilities")
        facility_string = ",".join(facilities)

        # -------------------------------
        # Occupancy Prices
        # -------------------------------

        single_price = request.form.get("single_price")
        double_price = request.form.get("double_price")
        triple_price = request.form.get("triple_price")
        quad_price = request.form.get("quad_price")

        new_hostel = Hostel(
            owner_id=session["user_id"],
            name=request.form["name"],
            location=request.form["location"],

            # Default price (used for listings)
            price=float(request.form["price"]),

            # Occupancy pricing
            single_price=float(single_price) if single_price else None,
            double_price=float(double_price) if double_price else None,
            triple_price=float(triple_price) if triple_price else None,
            quad_price=float(quad_price) if quad_price else None,

            gender=request.form["gender"],
            description=request.form["description"],
            image=None,
            map_link=request.form.get("map_link"),
            facilities=facility_string,
            rooms_available=(
                int(request.form.get("single_rooms") or 0) +
                int(request.form.get("double_rooms") or 0) +
                int(request.form.get("triple_rooms") or 0) +
                int(request.form.get("quad_rooms") or 0)
            ),
        )

        db.session.add(new_hostel)
        db.session.commit()
        
        # -----------------------------------
        # Create Occupancy Records Automatically
        # -----------------------------------

        occupancy_types = [
           ("Single Room", single_price, request.form.get("single_rooms")),
           ("Double Room", double_price, request.form.get("double_rooms")),
           ("Triple Room", triple_price, request.form.get("triple_rooms")),
           ("Quad Room", quad_price, request.form.get("quad_rooms")),
        ]


        for name, price, rooms in occupancy_types:

          if price and rooms and int(rooms) > 0:

            db.session.add(
                Occupancy(
                    hostel_id=new_hostel.id,
                    occupancy=name,
                    price=float(price),
                    rooms_available=int(rooms)
                )
            )

        db.session.commit()

        # -----------------------------------
        # Save Cover Image
        # -----------------------------------

        cover = request.files.get("image")

        if cover and cover.filename:

            if not allowed_file(cover.filename):
                flash("Only JPG, JPEG, PNG, and WEBP images are allowed.", "error")
                return redirect(request.url)

            ext = os.path.splitext(secure_filename(cover.filename))[1].lower()
            filename = str(uuid.uuid4()) + ext

            cover.save(
                os.path.join(upload_path, filename)
            )

            # Save as hostel cover
            new_hostel.image = filename

            # Save as first gallery image
            db.session.add(
                HostelImage(
                    hostel_id=new_hostel.id,
                    image=filename
                )
            )

        db.session.commit()

        # -----------------------------------
        # Save Gallery Images
        # -----------------------------------

        gallery = request.files.getlist("gallery")
        
        print("=" * 50)
        print("Cover:", request.files.get("image"))

        print("Gallery count:", len(gallery))

        for i, img in enumerate(gallery):
            print(f"{i}: {img.filename}")

        print("=" * 50)

        for img in gallery:

            if img and img.filename:

                if not allowed_file(img.filename):
                    continue

                ext = os.path.splitext(secure_filename(img.filename))[1].lower()
                gallery_name = str(uuid.uuid4()) + ext

                img.save(
                    os.path.join(upload_path, gallery_name)
                )

                hostel_image = HostelImage(
                    hostel_id=new_hostel.id,
                    image=gallery_name
                )

                db.session.add(hostel_image)

        db.session.commit()

        flash(
            "Hostel published successfully!",
            "success"
        )

        return redirect(
            url_for("hostel.my_hostels")
        )

    return render_template("add_hostel.html")


@hostel.route("/my-hostels")
def my_hostels():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    hostels = Hostel.query.filter_by(owner_id=session["user_id"]).all()

    return render_template("my_hostels.html", hostels=hostels)


@hostel.route("/hostel/<int:hostel_id>")
def hostel_details(hostel_id):
    """Retrieve and display details for a specific hostel including reviews."""
    hostel_obj = Hostel.query.get_or_404(hostel_id)

    reviews = hostel_obj.reviews

    print("=" * 50)
    print("Hostel:", hostel_obj.name)
    print("Images:", len(hostel_obj.images))

    for img in hostel_obj.images:
        print(img.image)

    print("=" * 50)

    return render_template(
        "hostel_details.html",
        hostel=hostel_obj,
        reviews=reviews
    )

@hostel.route("/edit-hostel/<int:hostel_id>", methods=["GET", "POST"])
def edit_hostel(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    hostel = Hostel.query.get_or_404(hostel_id)

    if hostel.owner_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("hostel.my_hostels"))

    if request.method == "POST":

        hostel.name = request.form.get("name")
        hostel.location = request.form.get("location")
        hostel.gender = request.form.get("gender")
        hostel.rooms_available = int(request.form.get("rooms_available"))
        hostel.description = request.form.get("description")
        hostel.map_link = request.form.get("map_link")
        

        # ==========================
        # Update Hostel Image
        # ==========================

        image = request.files.get("image")

        # Update cover image if a new one was uploaded
        if image and image.filename:

            if not allowed_file(image.filename):
                flash("Only JPG, JPEG, PNG, and WEBP images are allowed.", "error")
                return redirect(request.url)

            ext = os.path.splitext(secure_filename(image.filename))[1].lower()
            filename = str(uuid.uuid4()) + ext

            upload_path = os.path.join(
                current_app.static_folder,
                "uploads"
            )

            os.makedirs(upload_path, exist_ok=True)

            image.save(
                os.path.join(upload_path, filename)
            )

            hostel.image = filename

        db.session.commit()

        flash(
            "Hostel updated successfully!",
            "success"
        )

        return redirect(url_for("hostel.my_hostels"))

    return render_template(
        "edit_hostel.html",
        hostel=hostel
    )


@hostel.route("/delete-hostel/<int:hostel_id>", methods=["POST"])
def delete_hostel(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    hostel = Hostel.query.get_or_404(hostel_id)

    # Ensure only the owner can delete their hostel
    if hostel.owner_id != session["user_id"]:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("hostel.my_hostels"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('hostel.my_hostels'))

    # Delete favourites
    Favorite.query.filter_by(
        hostel_id=hostel.id
    ).delete()

    # Delete reviews
    Review.query.filter_by(
        hostel_id=hostel.id
    ).delete()

    # Delete bookings
    Booking.query.filter_by(
        hostel_id=hostel.id
    ).delete()

    # Delete hostel
    db.session.delete(hostel)

    db.session.commit()

    flash(
        "Hostel deleted successfully!",
        "success"
    )

    return redirect(
        url_for("hostel.my_hostels")
    )
    
@hostel.route("/approve-hostel/<int:hostel_id>", methods=["POST"])
def approve_hostel(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash("Unauthorized.", "danger")
        return redirect(url_for("home"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('admin_dashboard'))

    hostel_item = Hostel.query.get_or_404(hostel_id)

    hostel_item.status = "Approved"

    notification = Notification(
        user_id=hostel_item.owner_id,
        message=f"🎉 Your hostel '{hostel_item.name}' has been approved and is now visible to students."
    )

    db.session.add(notification)

    owner = User.query.get(hostel_item.owner_id)

    if owner:

        msg = Message(
            subject="HOSTEL SCOUT - Hostel Approved",
            recipients=[owner.email]
        )

        msg.body = f"""
Congratulations!

Your hostel "{hostel_item.name}" has been approved.

Students can now see and book your hostel.

Thank you for using HOSTEL SCOUT.
"""

        mail.send(msg)

    db.session.commit()

    flash("Hostel approved successfully.", "success")

    return redirect(url_for("admin_dashboard"))


@hostel.route("/reject-hostel/<int:hostel_id>", methods=["POST"])
def reject_hostel(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash("Unauthorized.", "danger")
        return redirect(url_for("home"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('admin_dashboard'))

    hostel_item = Hostel.query.get_or_404(hostel_id)

    hostel_item.status = "Rejected"

    notification = Notification(
        user_id=hostel_item.owner_id,
        message=f" Your hostel '{hostel_item.name}' was rejected. Please update it and submit again."
    )

    db.session.add(notification)

    owner = User.query.get(hostel_item.owner_id)

    if owner:

        msg = Message(
            subject="HOSTEL SCOUT - Hostel Rejected",
            recipients=[owner.email]
        )

        msg.body = f"""
Hello,

Unfortunately your hostel "{hostel_item.name}" was not approved.

Please update the listing and submit it again.

Thank you.
"""

        mail.send(msg)

    db.session.commit()

    flash("Hostel rejected successfully.", "warning")

    return redirect(url_for("admin_dashboard"))   