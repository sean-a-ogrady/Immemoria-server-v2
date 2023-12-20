from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from models.model_config import db
from models.base_validator_mixin import BaseValidatorMixin

class InputExchange(db.Model, SerializerMixin, BaseValidatorMixin):
    __tablename__ = "input_exchange_table"

    id = db.Column(db.Integer, primary_key=True)
    save_file_id = db.Column(db.Integer, db.ForeignKey("save_file_table.id"), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    action_type = db.Column(db.String(16), nullable=False) # Order, Chaos, Neutral, or Typed
    description = db.Column(db.String(2048), nullable=False)
    actions = db.Column(db.String(2048), nullable=False) # Stringified JSON
    summary = db.Column(db.String(2048), nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    openai_model = db.Column(db.String(32), nullable=False)
    prompt_tokens = db.Column(db.Integer, nullable=False)
    completion_tokens = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    serialize_rules = ("-save_file.input_exchanges",)

    save_file = db.relationship("SaveFile", back_populates="input_exchanges")

    def set_actions(self, actions_dict):
        self.actions = json.dumps(actions_dict)

    def get_actions(self):
        return json.loads(self.actions)

    @validates("prompt")
    def validate_prompt(self, key, prompt):
        return self.validate_string(key, prompt, max_length=500)

    @validates("action_type")
    def validate_action_type(self, key, action_type):
        return self.validate_choice(key, action_type, choices=["Order", "Chaos", "Neutral", "Typed"])

    @validates("description")
    def validate_description(self, key, description):
        return self.validate_string(key, description, max_length=2048)

    @validates("actions")
    def validate_actions(self, key, actions):
        return self.validate_string(key, actions, max_length=2048)

    @validates("summary")
    def validate_summary(self, key, summary):
        return self.validate_string(key, summary, max_length=2048)

    @validates("openai_model")
    def validate_openai_model(self, key, openai_model):
        return self.validate_string(key, openai_model, max_length=32)

    @validates("prompt_tokens")
    def validate_prompt_tokens(self, key, prompt_tokens):
        return self.validate_integer(key, prompt_tokens)

    @validates("completion_tokens")
    def validate_completion_tokens(self, key, completion_tokens):
        return self.validate_string(key, completion_tokens)

    @validates("cost")
    def validate_cost(self, key, cost):
        return self.validate_float(key, cost, min_value=0.0, decimal_points=2)