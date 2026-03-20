from flask import Flask
import os

from .extensions import db 
from datetime import timedelta

from app.home.routes import main_bp
from app.create.routes import create_bp
from app.sets.routes import sets_bp
from app.study.routes import study_bp
from app.users.routes import users_bp
from app.vocab.routes import vocab_bp
from app.api.routes import api_bp
from app.display import display_bp

from app.users.services import current_user

def create_app():
    app = Flask(__name__)

    app.secret_key = "dev"

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "sqlite:///" + os.path.join(app.root_path, "data", "full.db")
    )

    app.permanent_session_lifetime = timedelta(hours=1)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(sets_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(display_bp)
    
    app.register_blueprint(vocab_bp)

    app.context_processor(inject_user)
    

    return app


def inject_user():
    """ 
    Creates global user variable containing the user object 
    
    Returns a dict, but in templates, Jinja uses it as variable "user" with a User object

    rtype: dict
    """
    return dict(user=current_user())


