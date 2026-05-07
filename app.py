import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_migrate import Migrate

from models import db, User

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/users")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.cli.command("seed-db")
def seed_db():
    """Seed the database with sample users."""
    users_data = [
        {"username": "johndoe", "email": "john@example.com"},
        {"username": "janedoe", "email": "jane@example.com"},
        {"username": "bobsmith", "email": "bob@example.com"},
    ]

    for data in users_data:
        existing = User.query.filter(
            (User.username == data["username"]) | (User.email == data["email"])
        ).first()
        if not existing:
            user = User(username=data["username"], email=data["email"])
            db.session.add(user)

    db.session.commit()
    print(f"Seeded {len(users_data)} users.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=port, debug=debug)
