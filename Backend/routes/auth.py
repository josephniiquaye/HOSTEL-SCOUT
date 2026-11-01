import os
import uuid

from werkzeug.security import check_password_hash

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

import os

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User
from models.booking import Booking
from models.favorite import Favorite
from flask_mail import Message
from extensions import mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from app import limiter

auth = Blueprint("auth", __name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def allowed_file(filename):
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        allowed_roles = {"student", "owner"}
        if role not in allowed_roles:
            role = "student"

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role,
            is_verified=False
        )

        db.session.add(user)
        db.session.commit()

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        token = serializer.dumps(
            user.email,
            salt="email-confirm"
        )

        link = url_for(
            "verify_email",
            token=token,
            _external=True
        )

        msg = Message(
            subject="Verify your HOSTEL SCOUT account",
            recipients=[user.email]
        )

        msg.body = f"""
Welcome to HOSTEL SCOUT!

Please click the link below to verify your account:

{link}

This link expires in one hour.
"""
        try:
            mail.send(msg)

            flash(
                "Registration successful! Please check your email to verify your account.",
                "success"
            )

        except Exception as e:
            print("EMAIL ERROR:", e)

            flash(
                "Registration successful, but verification email could not be sent.",
                "warning"
            )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("10/minute")
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # User does not exist
        if not user:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        # Wrong password
        if not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        # Email not verified
        if not user.is_verified:
            flash(
                "Please verify your email before logging in. You can request a new verification email below.",
                "warning"
            )
            return redirect(url_for("auth.resend_verification"))

        # Login successful
        session["user_id"] = user.id
        session["role"] = user.role
        session["fullname"] = user.fullname

        flash("Welcome back!", "success")

        if user.role == "student":
            return redirect(url_for("student_dashboard"))

        elif user.role == "owner":
            return redirect(url_for("owner_dashboard"))

        elif user.role == "admin":
            return redirect(url_for("admin_dashboard"))

    return render_template("login.html")


@auth.route("/resend-verification", methods=["GET", "POST"])
@limiter.limit("5/hour")
def resend_verification():
    """Handle resending of email verification tokens for unverified users.

    Expects POST with 'email' form field. If the user exists and is not
    verified, generates a new timed token and (elsewhere) sends the
    verification email. Redirects and flashes messages for error/success
    cases.
    """

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:

            flash("No account exists with that email.", "danger")
            return redirect(url_for("auth.resend_verification"))

        if user.is_verified:

            flash("This account is already verified.", "info")
            return redirect(url_for("auth.login"))

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        token = serializer.dumps(
            user.email,
            salt="email-confirm"
        )

        link = url_for(
            "verify_email",
            token=token,
            _external=True
        )

        msg = Message(
            subject="HOSTEL SCOUT - Verify Your Email",
            recipients=[user.email]
        )

        msg.body = f"""
Hello {user.fullname},

You requested a new verification email.

Click the link below to verify your account.

{link}

This link expires in one hour.

HOSTEL SCOUT
"""

        try:

            mail.send(msg)

            flash(
                "A new verification email has been sent.",
                "success"
            )

        except Exception as e:

            print(e)

            flash(
                "Unable to send verification email.",
                "danger"
            )

        return redirect(url_for("auth.login"))

    return render_template("resend_verification.html")


@auth.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5/hour")
def forgot_password():
    """Handle forgot password requests and send reset emails."""

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if user:

            serializer = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"]
            )

            token = serializer.dumps(
                user.email,
                salt="password-reset"
            )

            link = url_for(
                "auth.reset_password",
                token=token,
                _external=True
            )

            msg = Message(
                subject="Reset your HOSTEL SCOUT password",
                recipients=[user.email]
            )

            msg.body = f"""
Hello {user.fullname},

Click the link below to reset your password:

{link}

This link expires in one hour.
"""

            try:
                mail.send(msg)

            except Exception as e:
                print(e)

        flash(
            "If that email address is registered, you will receive a password reset link shortly.",
            "info"
        )

        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=3600
        )

    except Exception:

        flash(
            "Reset link has expired.",
            "danger"
        )

        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()

    if not user:

        flash("User not found.", "danger")

        return redirect(url_for("auth.login"))

    if request.method == "POST":

        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password != confirm:

            flash("Passwords do not match.", "danger")

            return redirect(request.url)

        user.password = generate_password_hash(password)

        db.session.commit()

        flash(
            "Password changed successfully.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "reset_password.html",
        token=token
    )
    
    
@auth.route("/settings/delete-account", methods=["POST"])
def delete_account():
    """Permanently delete the current user's account and all associated data."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app import verify_csrf_token
    if not verify_csrf_token(request.form.get('csrf_token')):
        flash('Invalid CSRF token.', 'error')
        return redirect(url_for('auth.settings'))

    user_id = session["user_id"]
    user = User.query.get_or_404(user_id)

    # Cascade delete: bookings and favorites owned by this student.
    # Hostel-owned records (reviews, bookings, favorites, images, occupancies)
    # are handled by the SQLAlchemy cascade on the Hostel relationship.
    Booking.query.filter_by(student_id=user_id).delete()
    Favorite.query.filter_by(student_id=user_id).delete()

    # db.session.delete triggers cascade for hostels and notifications
    db.session.delete(user)
    db.session.commit()

    session.clear()
    flash("Your account has been deleted.", "info")
    return redirect(url_for("home"))


@auth.route("/settings", methods=["GET", "POST"])
def settings():
    """View and update the current user's settings.

    Requires a logged-in user stored in session['user_id']. Handles GET to
    render the settings page and POST to update fullname, phone, and email.
    """

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(session["user_id"])

    if request.method == "POST":

        user.fullname = request.form.get("fullname")
        user.phone = request.form.get("phone")
        user.email = request.form.get("email")

        db.session.commit()

        session["fullname"] = user.fullname

        flash(
            "Settings updated successfully.",
            "success"
        )

        return redirect(url_for("auth.settings"))

    return render_template(
        "settings.html",
        user=user
    )
    
    
@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(url_for("home"))

# =====================================================
# PROFILE
# =====================================================

@auth.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(session["user_id"])

    if request.method == "POST":

        fullname = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")

        if fullname:
            user.fullname = fullname

        if phone:
            user.phone = phone

        if email:
            existing = User.query.filter(
                User.email == email,
                User.id != user.id
            ).first()

            if existing:
                flash("Email already exists.", "danger")
                return redirect(url_for("auth.profile"))

            user.email = email

        image = request.files.get("profile_image")

        if image and image.filename:

            if not allowed_file(image.filename):
                flash("Only JPG, JPEG, PNG, and WEBP images are allowed.", "error")
                return redirect(url_for("auth.profile"))

            ext = os.path.splitext(secure_filename(image.filename))[1].lower()
            filename = str(uuid.uuid4()) + ext

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            image.save(
                os.path.join(upload_folder, filename)
            )

            user.profile_image = filename

        db.session.commit()

        session["fullname"] = user.fullname

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(url_for("auth.profile"))

    return render_template(
        "profile.html",
        user=user
    )

    
    