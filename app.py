from flask import Flask, make_response, session, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models.model_config import db

# Initialize Flask app and SQLAlchemy database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)
app.secret_key = "secret" # TODO: Change this to something more secure, like a randomly generated UUID

########################################################################
########################### API entry point ############################
########################################################################

# Auth test
@app.route("/api/auth_test", methods=["GET"])
def auth_test():
    """Test authentication."""
    pass


########################################################################
########################## Error Handling ##############################
########################################################################

# Error handling for 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


########################################################################
############################# Run the app ##############################
########################################################################

if __name__ == "__main__":
    app.run(debug=True, threaded=True)