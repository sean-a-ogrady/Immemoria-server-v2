from flask import Flask, make_response, session, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models.model_config import db
from auth.authorization_required import authorization_required
from routing.user_routes import UserRoutes
from models.database_models.user import User
from models.database_models.save_file import SaveFile
from models.database_models.input_exchange import InputExchange

# Initialize Flask app and SQLAlchemy database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)
CORS(app, supports_credentials=True)
app.secret_key = "secret" # TODO: Change this to something more secure, like a randomly generated UUID

only = () # TODO: Add fields to this tuple to limit the fields returned by the API

########################################################################
########################### API entry point ############################
########################################################################

@app.route("/")
@authorization_required
def index():
    return make_response({"msg": "API access granted.", "user": authorization.get_json()}, 200)

########################################################################
########################## Authorization ###############################
########################################################################

@app.route("/signup", methods=["POST"])
def add_user():
    payload = request.get_json()

    email_address = payload.get("email_address")
    username = payload.get("username")
    password = payload.get("password")

    # Call the add_user method from UserRoutes
    response = UserRoutes.add_user(email_address, username, password)
    return response


@app.route("/login", methods=["POST"])
def login_user():
    payload = request.get_json()

    matching_user = user.query.filter(user.email_address.like(f"%{payload['email_address']}%")).first()

    AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
        password=payload["password"].encode("utf-8"),
        hashed_password=matching_user.password.encode("utf-8")
    )

    if matching_user is not None and AUTHENTICATION_IS_SUCCESSFUL:
        session["user_id"] = matching_user.id
        return make_response({"message": "Login successful", "user": matching_user.to_dict(only=only)}, 200)
    else:
        return make_response({"error": "Invalid credentials."}, 401)


@app.route("/logout", methods=["DELETE"])
def logout_user():
    session["user_id"] = None
    return make_response({"message": "Logout successful"}, 200)

########################################################################
##################### Base Authorization Routes ########################
########################################################################

@app.route("/api/get_current_user", methods=["GET"])
@authorization_required
def get_current_user():
    return UserRoutes.get_current_user(session.get("user_id"))

########################################################################
########################### Admin Routes ###############################
########################################################################

@app.route("/api/users", methods=["GET"])
@authorization_required
def get_users():
    return UserRoutes.get_users()

########################################################################
########################## Error Handling ##############################
########################################################################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

########################################################################
############################# Run the app ##############################
########################################################################

if __name__ == "__main__":
    app.run(debug=True, threaded=True)