# backend/auth/utils/db.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"


#  Initialize the DB
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[✅] Database initialized.")


#  Get user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


#  Get user by ID
def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


#  Optional: Update user role
def update_user_role(user_id, new_role):
    user = get_user_by_id(user_id)
    if user:
        user.role = new_role
        db.session.commit()
        return True
    return False
