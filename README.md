# HOSTEL-SCOUT

HOSTEL-SCOUT is a Flask-based hostel booking and management platform for students, hostel owners, and administrators. The application helps students discover and compare hostels, book rooms, manage favorites, and monitor their stay, while providing owners and admins with tools to manage listings, requests, and approvals.

## Overview

This project is built as a full-stack web application with a Python backend and browser-based frontend templates. It includes a searchable hostel marketplace, role-based dashboards, booking workflows, reviews, announcements, and administrative moderation tools.

## Repository composition

This repository is primarily composed of:

- HTML: 40.3%
- Python: 37.5%
- CSS: 19.3%
- JavaScript: 2.7%
- Other: 0.2%

This aligns with the app's Python/Flask backend and HTML/CSS-based interface.

## Core features

### For students
- Browse approved hostel listings
- Search and filter by location, gender, rent, rating, and availability
- View hostel details, amenities, and photos
- Save favorites
- Submit booking requests
- Track booking status
- Leave reviews and ratings
- Receive notifications and platform announcements

### For hostel owners
- Add and manage hostel listings
- Update room availability and pricing
- Review student booking requests
- Monitor ownership-related data from a dashboard

### For administrators
- Review pending hostel submissions
- Approve or reject listings
- Moderate users and roles
- Publish announcements
- Review platform statistics and moderation information

## Tech stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- Flask-Mail
- Jinja2
- HTML, CSS, and JavaScript
- PostgreSQL-compatible database configuration
- Gunicorn for deployment

## Project structure

```text
HOSTEL-SCOUT/
├── Backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # App configuration and environment settings
│   ├── extensions.py           # SQLAlchemy, mail, and migration setup
│   ├── requirements.txt        # Python dependencies
│   ├── runtime.txt             # Runtime version for deployment
│   ├── Procfile                # Deployment process definition
│   ├── .env.example            # Sample .env template
│   ├── migrations/             # Database migration files
│   ├── models/                 # SQLAlchemy models
│   │   ├── announcement.py
│   │   ├── booking.py
│   │   ├── favorite.py
│   │   ├── hostel.py
│   │   ├── hostel_image.py
│   │   ├── notification.py
│   │   ├── occupancy.py
│   │   ├── review.py
│   │   └── user.py
│   ├── routes/                 # Flask blueprints for application logic
│   │   ├── auth.py
│   │   ├── booking.py
│   │   ├── favorite.py
│   │   ├── hostel.py
│   │   ├── notification.py
│   │   ├── pdf.py
│   │   └── review.py
│   ├── static/                 # CSS, JS, images, and uploaded media
│   ├── templates/              # Jinja templates
│   ├── uploads/                # Uploaded user and hostel files
│   └── .gitignore
├── README.md
├── fly.toml
├── render.yaml
├── .gitignore
└── LICENSE (if added later)
```

## Roles and access model

The platform supports three main roles:

- Student
- Owner
- Admin

These roles are enforced through route-level access control and role-aware dashboard behavior.

## Environment configuration

Create a `.env` file inside the `Backend` directory with the required values:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/hostel_scout
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-mail-password-here
MAIL_DEFAULT_SENDER=your-email@example.com
FLASK_DEBUG=0
```

Notes:
- `.env` should never be committed to version control.
- `DATABASE_URL` is required for database connectivity.
- If you use Gmail, an app-specific password may be required depending on your account security settings.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/josephniiquaye/HOSTEL-SCOUT.git
cd HOSTEL-SCOUT/Backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

From the `Backend` directory, start the app:

```bash
python app.py
```

You can also run it with Flask directly:

```bash
export FLASK_APP=app.py
flask run
```

The app runs in debug mode for local development unless configured otherwise.

## Database setup

The project includes Alembic migration files in `Backend/migrations`.

To initialize and apply migrations:

```bash
cd Backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

If migrations already exist, simply run:

```bash
flask db upgrade
```

## Deployment

This repository includes deployment configuration files for deployed hosting environments such as Render and Fly.io. The project is structured to support a production-ready deployment workflow with environment variables and process definitions.

## Future improvements

Potential enhancements for the project include:
- API documentation and endpoint references
- Payment and booking settlement integration
- Better mobile responsiveness
- More advanced analytics for owners and admins
- Automated testing and CI/CD
- Stronger production monitoring and logging

## License

No explicit license file is currently included in the repository. Unless a license is added later, the project should be treated as unlicensed.

## Maintainer

Repository maintained by `josephniiquaye`.

---

HOSTEL-SCOUT is designed to simplify hostel discovery and help manage accommodation bookings efficiently for both students and property owners.