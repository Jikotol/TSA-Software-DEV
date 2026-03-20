from flask import Blueprint, request, render_template, redirect, url_for
import json
from .services import find_main_gloss, get_main_head_tuples

main_bp = Blueprint("home", __name__, template_folder="templates")

@main_bp.route("/", methods=["POST", "GET"])
@main_bp.route("/home", methods=["POST", "GET"])
@main_bp.route("/index", methods=["POST", "GET"])
def home():
    """ Handles home.html rendering and handles redirections from the search bar """
    # Search bar results
    if request.method == "POST":
        search = request.form["search"]

        # Searches with heuristics in order to find the gloss they want
        main_gloss_list = find_main_gloss(search)

        if len(main_gloss_list) == 1:
            # Redirects user straight tothe vocab page
            main_gloss = main_gloss_list[0]
            return redirect(url_for("vocab.vocab", main_gloss_id=main_gloss._id, gloss_id=main_gloss.head_gloss_id))

        elif main_gloss_list:
            # Redirects user to search selection page
            return render_template("home/search_results.html", search=search, main_gloss_results=main_gloss_list)

        else:
            return render_template(
                "error.html", 
                title="Search not found", 
                msg=f"No results for \"{request.form["search"]}\""
            )

    # Gets random main glosses their head glosses for video browsing on homepage
    random_vid_tuples = get_main_head_tuples(8)

    random_word_tuples = get_main_head_tuples(40)


    return render_template(
                "home/home.html", 
                random_vid_tuples=random_vid_tuples, 
                random_word_tuples=random_word_tuples
            )
