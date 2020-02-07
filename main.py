import os
import structlog

from flask import Flask

from flask_cors import CORS

from database import db, User, Todo

from version import VERSION

logger = structlog.get_logger(__name__)

# Create app
app = Flask(__name__, static_url_path="/static")
app.url_map.strict_slashes = False

# NOTE: the extra headers need to be available in the API gateway: that is handled by zappa_settings.json
CORS(
    app,
    supports_credentials=True,
    resources="/*",
    allow_headers="*",
    origins="*",
    expose_headers="Authorization,Content-Type,Authentication-Token,Quick-Authentication-Token,Content-Range",
)
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://workshop:workshop@localhost/workshop")
app.config["DEBUG"] = False if not os.getenv("DEBUG") else True
app.config["SECRET_KEY"] = (
    os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else "super-secret"
)

app.config["VERSION"] = VERSION
app.config["FLASK_ADMIN_SWATCH"] = "flatly"
app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
app.config["SECRET_KEY"] = (
    os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else "super-secret"
)
app.config["SECURITY_PASSWORD_HASH"] = "pbkdf2_sha256"
app.config["SECURITY_PASSWORD_SALT"] = (
    os.getenv("SECURITY_PASSWORD_SALT")
    if os.getenv("SECURITY_PASSWORD_SALT")
    else "SALTSALTSALT"
)
# More Flask Security settings
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_CONFIRMABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True
app.config["SECURITY_CHANGEABLE"] = True
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = ["email", "username"]
app.config["SECURITY_BACKWARDS_COMPAT_AUTH_TOKEN"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Replace the next six lines with your own SMTP server settings
app.config["SECURITY_EMAIL_SENDER"] = (
    os.getenv("SECURITY_EMAIL_SENDER")
    if os.getenv("SECURITY_EMAIL_SENDER")
    else "no-reply@example.com"
)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "localhost")
app.config["MAIL_PORT"] = 1025 if app.config["MAIL_SERVER"] == "localhost" else 456
app.config["MAIL_USE_SSL"] = False if app.config["MAIL_SERVER"] == "localhost" else True
app.config["MAIL_USERNAME"] = (
    os.getenv("MAIL_USERNAME") if os.getenv("MAIL_USERNAME") else None
)
app.config["MAIL_PASSWORD"] = (
    os.getenv("MAIL_PASSWORD") if os.getenv("MAIL_PASSWORD") else None
)

# Needed for easier REST token login
app.config["WTF_CSRF_ENABLED"] = False


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


db.init_app(app)

@app.route("/")
def hello():
    user = User.query.first()
    todo = Todo.query.first()
    return f"Hello World! DB Check -> First user: {user.username}, First tag: {todo.name}"


if __name__ == "__main__":
    app.run()
