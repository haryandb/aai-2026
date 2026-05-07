import click
from models import db, User


def seed_db_command():
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
    click.echo(f"Seeded {len(users_data)} users.")


def register_commands(app):
    """Register seeder commands to Flask app."""

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with sample users."""
        seed_db_command()
