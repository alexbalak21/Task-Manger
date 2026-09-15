import os
import datetime

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-min-32-bytes")
    
    # Database Configuration (MySQL)
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "mydatabase")

    # MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"\
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    
    # For SQLite (comment out PostgreSQL URI above if using SQLite)
    # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret-key-min-32-bytes")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    STATIC_FOLDER = os.getenv("STATIC_FOLDER", "frontend")
    STATIC_URL_PATH = os.getenv("STATIC_URL_PATH", "")

    # Mail (AlwaysData SMTP, or any standard SMTP relay)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp-<account>.alwaysdata.net")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@example.com")
    # If unset (e.g. local dev), emails are logged to the console instead of sent
    MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", "false").lower() == "true"

    # Used to build links inside emails (invite links, etc.)
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
