from flask import Blueprint, render_template, redirect, url_for, session, request, flash
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


@notification.route("/notification/read/<int:id>", methods=["POST"])
def mark_read(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('notification.notifications'))

    notif = Notification.query.get_or_404(id)

    if notif.user_id != session["user_id"]:
        return redirect(url_for("notification.notifications"))

    notif.is_read = True

    db.session.commit()

    return redirect(url_for("notification.notifications"))


@notification.route("/notification/delete/<int:id>", methods=["POST"])
def delete_notification(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('notification.notifications'))

    notif = Notification.query.get_or_404(id)

    if notif.user_id != session["user_id"]:
        return redirect(url_for("notification.notifications"))

    db.session.delete(notif)

    db.session.commit()

    return redirect(url_for("notification.notifications"))