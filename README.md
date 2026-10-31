# HOSTEL-SCOUT

A professional Flask-based hostel booking and management platform designed for students, hostel owners, and administrators.

HOSTEL-SCOUT helps students discover reliable accommodation options, compare listings, and book rooms, while giving hostel owners a central place to manage properties, availability, and bookings. Admins can moderate the platform, review listings, and manage user activity from a dedicated dashboard.

## Overview

This project is a full-stack web application built with Python and Flask. It combines a searchable marketplace, role-based dashboards, notifications, reviews, and booking workflows into a single platform for student accommodation management.

### Primary goals
- Simplify hostel discovery for students
- Provide a clear online marketplace for accommodation listings
- Enable owners to manage their hostels efficiently
- Give admins tools to moderate and monitor the platform

## Key Features

### For Students
- Browse approved hostels on the homepage
- Search and filter properties by location, gender, price, rating, and availability
- View hostel details, photos, and amenities
- Save properties as favorites
- Submit booking requests
- Track booking status
- Leave reviews and ratings
- Receive notifications and announcements

### For Owners
- List and manage hostel properties
- Update room availability and pricing
- Handle booking requests from students
- Monitor owner-specific metrics from a dashboard

### For Admins
- Review pending hostel submissions
- Approve or reject listings
- Manage platform users and roles
- Publish announcements to all users
- Review key application statistics and moderation data

## Tech Stack

- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate / Alembic
- Flask-Mail
- Jinja2
- HTML, CSS, and JavaScript
- SQLite / PostgreSQL-compatible database configuration

## Project Structure

```text
HOSTEL-SCOUT/
├── Backend/
│   ├── app.py                    # Main Flask application entry point
│   ├── config.py                 # Environment-based app configuration
│   ├── extensions.py             # Database, mail, and migration setup
│   ├── requirements.txt          # Python package dependencies
│   ├── runtime.txt               # Runtime version for deployment
│   ├── Procfile                  # Hosting process definition
│   ├── models/                   # SQLAlchemy models
│   │   ├── announcement.py
│   │   ├── booking.py
│   │   ├── favorite.py
│   │   ├── hostel.py
│   │   ├── hostel_image.py
│   │   ├── notification.py
│   │   ├── occupancy.py
│   │   ├── review.py
│   │   └── user.py
│   ├── routes/                   # Flask blueprints for app logic
│   │   ├── auth.py
│   │   ├── booking.py
│   │   ├── favorite.py
│   │   ├── hostel.py
│   │   ├── notification.py
│   │   ├── pdf.py
│   │   └── review.py
│   ├── migrations/               # Alembic migration files
│   ├── static/                   # CSS, JS, images, and uploaded assets
│   ├── templates/                # Jinja HTML templates
│   ├── uploads/                 # Media upload directory
│   └── .env.example              # Example environment file
├── README.md
├── .gitignore
└── LICENSE (if added later)
```

## Roles and Access Model

The application supports three user categories:

- Student
- Owner
- Admin

These roles are enforced through route-level logic and dashboard permissions, ensuring the right users can access the right features.

## Environment Configuration

Create a `.env` file inside the `Backend` directory with the following values:

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

### Notes
- The app uses `python-dotenv` to load environment variables.
- `DATABASE_URL` is required for database connectivity.
- If using Gmail, you may need an app-specific password depending on your account security settings.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/josephniiquaye/HOSTEL-SCOUT.git
cd HOSTEL-SCOUT/Backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

Start the app from the `Backend` directory:

```bash
python app.py
```

The application will run in debug mode for local development.

Alternative:

```bash
export FLASK_APP=app.py
flask run
```

## Database Setup

The project includes Alembic migration scripts in `Backend/migrations/`.

To initialize and apply migrations:

```bash
cd Backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

If migrations are already present, you can usually run only:

```bash
flask db upgrade
```

## Deployment Notes

The repository includes a `Procfile` and `runtime.txt`, which suggests it was intended for deployment on a platform such as Heroku or another PaaS provider. For production deployment, environment variables, database configuration, and security settings should be reviewed carefully.

## Key Implementation Details

- Homepage filters and sorting logic support hostel discovery and comparison.
- The app includes email verification using signed tokens.
- Notifications are created when announcements are published.
- Booking and approval workflows are role-aware.
- Static assets and templates are separated for cleaner front-end organization.

## Future Improvements

This project could be improved with:
- API documentation and endpoint references
- Payment integration for bookings
- More advanced analytics for owners and admins
- Better mobile responsiveness
- Automated testing
- CI/CD and production deployment pipeline setup

## License

No explicit license file was found in this repository. Unless the owner adds one later, the project should be treated as unlicensed.

## Maintainer

Repository maintained by `josephniiquaye`.

---

This README provides a clear overview of the HOSTEL-SCOUT project, its architecture, and how to run it locally.
