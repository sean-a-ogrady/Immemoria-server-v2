from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from models.model_config import db
from models.base_validator_mixin import BaseValidatorMixin

class SaveFile(db.Model, SerializerMixin, BaseValidatorMixin):
    __tablename__ = "save_file_table"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    save_name = db.Column(db.String(32), nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    serialize_rules = ("-user.save_files", "-input_exchanges.save_file")

    user = db.relationship("User", back_populates="save_files")

    input_exchanges = db.relationship("InputExchange", back_populates="save_file")

    @validates("save_name")
    def validate_save_name(self, key, save_name):
        return self.validate_string(key, save_name, max_length=32)