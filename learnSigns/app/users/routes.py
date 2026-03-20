from flask import Blueprint, session, request, redirect, url_for, render_template
from .services import sign_in, add_user

users_bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@users_bp.route("/", methods=["POST", "GET"])
@users_bp.route("/login", methods=["POST", "GET"])
def login():
    """
    Renders "login" template and handles account creation and user sign in

    rtype: str - HTML string for "login.html" | Response - redirect to "home"
    """

    if request.method == "POST" and request.form["nm"]:
        # Makes the current session continue after the browser is closed, keeping users signed in
        session.permanent = True

        username = request.form["nm"]

        # Creates a new account for user under the given username if the account does not exist
        if not sign_in(username):
            add_user(username)
            sign_in(username)
        else:
            # Signs in user if account is found
            sign_in(username)

        # Brings user to home page
        return redirect(url_for("home.home"))

    # Makes sure session is updated correctly and redirects signed in user away from login page
    if "username" in session:
        sign_in(session["username"])
        return redirect(url_for("home.home"))

    # Renders "login.html" for users to sign in
    return render_template("users/login.html")
    
@users_bp.route("/logout")
def logout():
    """ 
    Logs current user out by updating session data 
    
    rtype: Response 
    """

    # Updates session variables relating to user
    if "user_id" in session:
        del session["user_id"] 
    if "username" in session:
        del session["username"]
    
    # Redirects user to "login.html" for logging in 
    return redirect(url_for("users.login"))

@users_bp.route("/profile")
def profile():
    return render_template("users/profile.html")
