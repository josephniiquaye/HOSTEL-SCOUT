# HOSTEL-SCOUT

HOSTEL-SCOUT is a Flask-based hostel booking and management web application designed to help students find suitable accommodation and help hostel owners/admins manage their listings and bookings.

The project includes a public marketplace for approved hostels, user authentication, role-based dashboards, booking workflows, notifications, reviews, and admin moderation.

## Overview

This repository contains a complete web app for:

- Students searching for hostels
- Hostel owners listing and managing their properties
- Admins approving listings, monitoring users, and publishing announcements
- Email-based account verification and password reset workflows

## Tech Stack

- Python
- Flask
- SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-Mail
- Jinja2 templates
- HTML, CSS, JavaScript
- PostgreSQL/MySQL-compatible database via SQLAlchemy connection string

## Project Structure

```text
HOSTEL-SCOUT/
├── Backend/
│   ├── app.py                  # Main Flask application entry point
│   ├── config.py               # App configuration and environment settings
│   ├── extensions.py           # Flask extensions registration
│   ├── requirements.txt        # Python dependencies
│   ├── runtime.txt             # Deployment runtime version
│   ├── Procfile                # Heroku-style process configuration
│   ├── models/                 # Database models
│   │   ├── user.py
│   │   ├── hostel.py
│   │   ├── booking.py
│   │   ├── review.py
│   │   ├── favorite.py
│   │   ├── notification.py
│   │   ├── occupancy.py
│   │   ├── announcement.py
│   │   └── hostel_image.py
│   ├── routes/                 # Route blueprints for app features
│   │   ├── auth.py
│   │   ├── hostel.py
│   │   ├── booking.py
│   │   ├── review.py
│   │   ├── favorite.py
│   │   ├── notification.py
│   │   └── pdf.py
│   ├── migrations/             # Alembic migration files
│   ├── static/                 # CSS, JS, images, uploads
│   ├── templates/              # Jinja templates for frontend pages
│   └── uploads/                # Uploaded hostel media storage
└── README.md
```

## Core Features

### For Students
- Browse hostels on the homepage
- Search and filter by location, gender, price, availability, and rating
- View hostel details and photos
- Add hostels to favorites
- Book available rooms
- Leave reviews and ratings
- Track notifications and announcements

### For Owners
- Add and manage hostel listings
- Update hostel details and availability
- View bookings received for their properties
- Monitor website activity from a dashboard

### For Admins
- Review pending hostel submissions
- Approve or reject hostel listings
- Manage users and bookings
- Publish announcements to all users
- Monitor app statistics and dashboard data

## App Roles

The application supports three main user roles:

- Student
- Owner
- Admin

Role-based access is enforced in several routes and dashboard views.

## Environment Variables

Create a `.env` file in the `Backend` directory and define values like:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///hostel_scout.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=your_email@example.com
```

Notes:
- The app loads environment variables using `python-dotenv`.
- If `DATABASE_URL` is not set, the app may not connect to a database properly.
- For Gmail, you may need an app password depending on your account security settings.

## Installation

From the project root:

```bash
cd Backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

From the `Backend` folder:

```bash
python app.py
```

The app will start in debug mode by default.

Optional alternative:

```bash
export FLASK_APP=app.py
flask run
```

## Database Setup

This project includes Alembic migrations under `Backend/migrations/`.

To initialize or apply migrations:

```bash
cd Backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

If migrations are already prepared in the project, you may only need to run:

```bash
flask db upgrade
```

## Notes

- The app’s homepage filters and searches hostels by several criteria.
- There is an email verification flow using a signed token.
- The project includes PDF-related functionality under `routes/pdf.py`.
- The app appears to be designed for deployment on a hosting platform such as Heroku, as shown by `Procfile` and `runtime.txt`.

## Future Improvements

Possible enhancements for this project include:

- Better API documentation
- Payment integration for bookings
- More detailed owner analytics
- Mobile responsiveness improvements
- Deployment setup for production environments
- Automated tests

## License

No explicit license file was found in the repository, so the project should be treated as unlicensed unless otherwise stated by the owner.

## Maintainer

This project appears to be maintained by the repository owner under the GitHub account `josephniiquaye`.

---

This README was created to help new contributors and users understand the purpose, structure, and setup of the project.
