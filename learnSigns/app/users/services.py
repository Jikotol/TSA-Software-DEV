from flask import session
from app.extensions import db
from app.models import User

def sign_in(name):
    """
    Updates session variables to sign the user in

    rtype: None | False
    """
    # Gets user object associated with given username
    found_user = User.query.filter_by(username=name).first()

    # Signs in user by updating session variables
    if found_user:
        session["user_id"] = found_user._id
        session["username"] = found_user.username
    else:
        return False

def add_user(username):
    """ Adds new user to the database """
    user = User(username)
    db.session.add(user)
    db.session.commit()

def current_user():
    """ 
    Returns the current user's User object 
    
    rtype: User | None
    """
    if "user_id" in session:
        return User.query.filter_by(_id=session["user_id"]).first()
    return None
