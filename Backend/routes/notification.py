from flask import Blueprint, render_template, redirect, url_for, session
from extensions import db
from models.notification import Notification

notification = Blueprint("notification", __name__)


@notification.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    notifications = Notification.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Notification.created_at.desc()).all()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@notification.route("/notification/read/<int:id>")
def mark_read(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    notification = Notification.query.get_or_404(id)

    if notification.user_id != session["user_id"]:
        return redirect(url_for("notification.notifications"))

    notification.is_read = True

    db.session.commit()

    return redirect(url_for("notification.notifications"))


@notification.route("/notification/delete/<int:id>")
def delete_notification(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    notification = Notification.query.get_or_404(id)

    if notification.user_id != session["user_id"]:
        return redirect(url_for("notification.notifications"))

    db.session.delete(notification)

    db.session.commit()

    return redirect(url_for("notification.notifications"))