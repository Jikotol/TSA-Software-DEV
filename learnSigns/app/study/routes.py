from flask import Blueprint, render_template

study_bp = Blueprint("study", __name__, url_prefix="/study", template_folder="templates", static_folder="static", static_url_path="/study/static")

@study_bp.route("/<string:mode>/<int:set_id>") 
def study(set_id, mode):
    """
    Renders the study template
    
    set_id: int
    rtype: str - HTML string for "study.html"
    """
    if mode == "review":
        return render_template("study/review.html", review=True)
    else:
        return render_template("study/learn.html")
