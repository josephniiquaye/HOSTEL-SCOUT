# =============================================================================
# SECURITY WARNING
# =============================================================================
# The .env file in this directory contains LIVE credentials (secret keys,
# mail passwords, database URLs, etc.).
#
#   1. NEVER commit .env to version control. It is listed in .gitignore.
#   2. All credentials in .env MUST be rotated if they have ever been
#      exposed (e.g. accidentally committed, shared, or pushed to a repo).
#   3. Use .env.example (placeholder values only) as the reference template
#      for other developers setting up the project.
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    _secret_key = os.getenv("SECRET_KEY")
    if not _secret_key:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set. "
            "Please set it before running the application."
        )
    SECRET_KEY = _secret_key

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = os.getenv(
        "MAIL_USE_TLS",
        "True"
    ) == "True"

    MAIL_USE_SSL = False


    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )