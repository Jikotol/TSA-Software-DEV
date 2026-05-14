from flask import Blueprint, render_template

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz", template_folder="templates", static_folder="static", static_url_path="/quiz/static")


@quiz_bp.route("/<int:set_id>")
def quiz(set_id):
    return render_template("quiz/quiz.html", setId = set_id)