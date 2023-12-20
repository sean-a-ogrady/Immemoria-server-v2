from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from models.model_config import db
from models.base_validator_mixin import BaseValidatorMixin
from models.database_models.save_file import SaveFile
from models.database_models.input_exchange import InputExchange

class User(db.Model, SerializerMixin, BaseValidatorMixin):
    __tablename__ = "user_table"
    
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) # Hashed password
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime, server_default=db.func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # NOTE: Not for demo version:
    # openai_api_key = db.Column(db.String(255), nullable=True) # Hashed API key
    # free_trial = db.Column(db.Boolean, nullable=False, default=True)

    serialize_rules = ("-password", "-is_admin", "-openai_api_key", "-free_trial", "-save_files.user")

    save_files = db.relationship("SaveFile", back_populates="user")

    @validates("email_address")
    def validate_email_address(self, key, email_address):
        return self.validate_string(key, email_address, max_length=255)

    @validates("username")
    def validate_username(self, key, username):
        return self.validate_string(key, username, max_length=32)
    
    @validates("password")
    def validate_password(self, key, password):
        return self.validate_string(key, password, max_length=255)
    
    @validates("is_admin")
    def validate_is_admin(self, key, is_admin):
        return self.validate_boolean(key, is_admin)