from flask import Blueprint

display_bp = Blueprint("display", __name__, static_folder="static", static_url_path="/display/static", template_folder="templates")