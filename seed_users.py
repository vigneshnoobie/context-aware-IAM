from app import create_app
from backend.auth.utils.db import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()  

    users = [
        {"email": "admin@example.com", "password": "Admin@123", "role": "admin"},
        {"email": "user1@example.com", "password": "User@123", "role": "user"},
        {"email": "user2@example.com", "password": "User@123", "role": "user"},
    ]

    for user in users:
        existing = User.query.filter_by(email=user["email"]).first()
        if not existing:
            new_user = User(
                email=user["email"],
                password_hash=generate_password_hash(user["password"]),
                role=user["role"]
            )
            db.session.add(new_user)

    db.session.commit()
    print("✅ Users seeded into users.db")
