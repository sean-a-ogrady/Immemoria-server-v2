from flask import Flask, request, make_response, jsonify
from models.model_config import db
from models.database_models.user import User
from sqlalchemy.exc import IntegrityError
import bcrypt
import re

class UserRoutes():
    """Logic for handling user routes"""

    @staticmethod
    def add_user(email_address, username, password):
        """Add a user to the database"""
        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Check for valid email address
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email_address):
                return make_response({"message": "Invalid email address."}, 400)

            # Create a new user object
            new_user = User(
                email_address=email_address,
                username=username,
                password=hashed_password
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return make_response({"message": "User created successfully", "user": new_user.to_dict(only=only)}, 201)
        except IntegrityError:
            db.session.rollback()
            return make_response({"message": "User already exists"}, 409)
        except ValueError:
            db.session.rollback()
            return make_response({"message": "Invalid request"}, 400)

    @staticmethod
    def get_current_user(user_id):
        """Get the current user by session ID from the database"""
        try:
            current_user = User.query.filter(User.id == user_id).first()
            if current_user is None:
                return make_response({"message": "User not found"}, 404)
            return make_response({"message": "User retrieved successfully", "user": current_user.to_dict(only=only)}, 200)
        except Exception as error:
            return make_response({"message": "Something went wrong", "details": str(error)}, 500)