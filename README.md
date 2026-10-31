# HOSTEL-SCOUT

HOSTEL-SCOUT is a Flask-based hostel booking and management web application designed to help students discover suitable accommodation and help hostel owners manage listings, bookings, and property operations more efficiently.

The project combines search, filtering, booking flows, notifications, reviews, and admin moderation into a single campus accommodation platform. It supports three distinct user types: students, hostel owners, and administrators.

## Project purpose

This application is intended to simplify hostel discovery and management by giving students an easy way to compare and book accommodation, while allowing owners to list and manage their hostels from one dashboard.

## Main features

### Student features
- Browse a homepage of approved hostels
- Search and filter hostels by name, location, gender, price, and availability
- View detailed hostel information and gallery images
- Save hostels to favorites
- Book accommodations and track booking status
- Leave reviews and ratings
- Receive notifications and platform announcements

### Owner features
- Create and manage hostel listings
- Update availability and pricing information
- View incoming booking requests
- Manage their own dashboard metrics and hostel portfolio

### Admin features
- Review and approve pending hostel submissions
- Manage users and roles
- Review bookings and platform activity
- Publish announcements to all users
- View summary statistics for the platform

## Tech stack

- Python
- Flask
- SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-Mail
- Jinja2 templates
- HTML, CSS, and JavaScript
- SQLite/PostgreSQL-compatible database via SQLAlchemy

## Repository structure

```text
HOSTEL-SCOUT/
├── Backend/
│   ├── app.py                  # Main Flask application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── extensions.py           # Flask extension setup
│   ├── requirements.txt        # Python dependencies
│   ├── runtime.txt             # Deployment runtime version
│   ├── Procfile                # Hosting process definition
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
│   ├── routes/                 # Flask blueprints for app features
│   │   ├── auth.py
│   │   ├── booking.py
│   │   ├── favorite.py
│   │   ├── hostel.py
│   │   ├── notification.py
│   │   ├── pdf.py
│   │   └── review.py
│   ├── migrations/             # Alembic database migration scripts
│   ├── static/                 # CSS, JS, images, and uploads
│   ├── templates/              # HTML templates for pages and dashboards
│   └── uploads/                # Uploaded media directory
├── README.md
├── .gitignore
└── .env.example (if present in the app template folder)
```

## App roles

The application explicitly supports these roles:

- Student
- Owner
- Admin

Access is role-aware in several dashboard and management routes, which prevents unauthorized users from viewing privileged pages.

## Environment variables

Create a `.env` file inside the `Backend` directory with values like:

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
- The app loads environment variables using `python-dotenv`.
- `DATABASE_URL` is essential for connecting to the database.
- For Gmail-based email sending, an app password may be required depending on account security settings.

## Installation

From the repository root:

```bash
cd Backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

From the `Backend` directory:

```bash
python app.py
```

The app runs in debug mode by default for local development.

Alternative:

```bash
export FLASK_APP=app.py
flask run
```

## Database setup

The project includes Alembic migrations under `Backend/migrations/`.

To initialize and apply migrations:

```bash
cd Backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

If migration files already exist, you may only need:

```bash
flask db upgrade
```

## Deployment notes

The presence of `Procfile` and `runtime.txt` suggests this application was designed for deployment on a platform like Heroku or another cloud-based PaaS. For production use, environment variables and the database configuration should be reviewed carefully.

## Notable implementation details

- The homepage supports hostel filtering and sorting.
- The system includes email verification using token-based signing.
- Notifications are generated when admin announcements are created.
- The app includes PDF-related routes in `routes/pdf.py`.
- Front-end pages and assets are separated into `templates/` and `static/`.

## Possible improvements

This project could be enhanced with:

- API documentation and endpoints reference
- Payment integration for bookings
- More advanced dashboard analytics
- Improved mobile responsiveness
- Automated testing
- Production deployment configuration and CI setup

## License

No explicit license file was found in this repository, so it should be treated as unlicensed unless the owner specifies otherwise.

## Maintainer

This project appears to be maintained by the repository owner, `josephniiquaye`.

---

This README is intended to help contributors and users quickly understand the purpose, architecture, and local setup of the HOSTEL-SCOUT project.
