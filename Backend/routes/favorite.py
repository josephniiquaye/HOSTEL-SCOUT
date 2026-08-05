from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    render_template
)

from extensions import db
from models.favorite import Favorite
from models.hostel import Hostel

favorite = Blueprint("favorite", __name__)


@favorite.route("/favorite/<int:hostel_id>")
def add_favorite(hostel_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Only students can save favorites
    if session.get("role") != "student":
        flash("Only students can save favorites.", "warning")
        return redirect(url_for("hostel.hostel_details", hostel_id=hostel_id))

    hostel = Hostel.query.get_or_404(hostel_id)

    existing = Favorite.query.filter_by(
        student_id=session["user_id"],
        hostel_id=hostel.id
    ).first()

    if existing:
        flash("Hostel already in your favorites.", "info")
        return redirect(url_for("hostel.hostel_details", hostel_id=hostel.id))

    fav = Favorite(
        student_id=session["user_id"],
        hostel_id=hostel.id
    )

    db.session.add(fav)
    db.session.commit()

    flash("Hostel added to favorites.", "success")

    return redirect(url_for("hostel.hostel_details", hostel_id=hostel.id))


@favorite.route("/my-favorites")
def my_favorites():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    favorites = Favorite.query.filter_by(
        student_id=session["user_id"]
    ).all()

    return render_template(
        "my_favorites.html",
        favorites=favorites
    )


@favorite.route("/remove-favorite/<int:favorite_id>")
def remove_favorite(favorite_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    favorite = Favorite.query.get_or_404(favorite_id)

    if favorite.student_id != session["user_id"]:
        flash("Unauthorized.", "danger")
        return redirect(url_for("favorite.my_favorites"))

    db.session.delete(favorite)
    db.session.commit()

    flash("Favorite removed.", "success")

    return redirect(url_for("favorite.my_favorites"))