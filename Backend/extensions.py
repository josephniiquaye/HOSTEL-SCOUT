"""Flask extensions for database, migrations and mail."""

from typing import TYPE_CHECKING

# -------------------------------
# SQLAlchemy
# -------------------------------
if TYPE_CHECKING:
    from typing import Any

    SQLAlchemy = Any
else:
    try:
        from importlib import import_module

        sqlalchemy_module = import_module("flask_sqlalchemy")
        SQLAlchemy = sqlalchemy_module.SQLAlchemy
    except (ImportError, AttributeError):
        class SQLAlchemy:  # pylint: disable=too-few-public-methods
            """Fallback stub for Flask-SQLAlchemy
            when the package is unavailable."""

            def __init__(self, *a, **kw):
                pass

            def init_app(self, _app):
                """No-op initialization for the fallback SQLAlchemy stub."""
                return None


# -------------------------------
# Flask-Migrate
# -------------------------------
if TYPE_CHECKING:
    from typing import Any

    Migrate = Any
else:
    try:
        from flask_migrate import Migrate
    except ImportError:
        class Migrate:
            """Fallback stub for Flask-Migrate when the package is unavailable."""

            def __init__(self, *_args, **_kwargs):
                pass

            def init_app(self, _app=None, **_kwargs):
                """No-op initialization for the fallback Migrate stub."""
                return None


# -------------------------------
# Flask-Mail
# -------------------------------
if TYPE_CHECKING:
    from typing import Any

    Mail = Any
else:
    try:
        from flask_mail import Mail
    except ImportError:
        class Mail:  # pylint: disable=too-few-public-methods
            """Fallback stub for Flask-Mail when the package is unavailable."""

            def __init__(self, *a, **kw):
                pass

            def init_app(self, _app=None):
                """No-op initialization for the fallback Mail stub."""
                return None


# -------------------------------
# Extensions
# -------------------------------
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()