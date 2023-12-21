from flask import make_response, session
from models.model_config import db
from models.database_models.user import User
from functools import partial, wraps

#######################################################
################ AUTHORIZATION LEVELS #################
#######################################################

# BASE_AUTHORIZED_OPERATIONS=[] # TODO
# ADMIN_AUTHORIZED_OPERATIONS=["get_users"] # TODO

#######################################################
###### EXPORTABLE MIDDLEWARE UTILITY FUNCTION(S) ######
#######################################################

def authorization_required(func=None):

    # Factory function to tether wrapper to decorator.
    @wraps(func)

    # Inner authorization function.
    def decorated_authorizer(*args, **kwargs):
        # Retrieve existing and matching user ID from server-persistent session storage.
        # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
        user_id = session.get("user_id")

        if not user_id:
            return make_response({"error": "User account not authenticated. Please log in or sign up to continue using the application."}, 401)
            
        try:
            # Query users from database where authorized user exists (has matching ID).
            authorized_user = User.query.filter(User.id == user_id).first()
            if authorized_user is None:
                return make_response({"error": "Invalid username or password. Try again."}, 401)
        except Exception as error:
            return make_response({"error": f"Something went wrong.", "details": str(error)}, 500)

        # Invoke wrapped view function with administrative access as output.
        # return func(authorized_user.to_dict(), *args, **kwargs)
        return func(*args, **kwargs)
    return decorated_authorizer

"""
Check level of user
make variable BASE_AUTHORIZED_OPERATIONS=["auth_test"] and ADMIN_AUTHORIZED_OPERATIONS
do the checking logic
func.__name__ == "auth_test"
"""